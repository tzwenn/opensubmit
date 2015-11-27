'''
    Tets cases focusing on the frontend views ('GET') accessed by students.
'''

from django.contrib.auth.models import User

from opensubmit.tests.cases import SubmitTestCase

from opensubmit.models import Course, Assignment, Submission
from opensubmit.models import Grading, GradingScheme
from opensubmit.models import UserProfile

class StudentDisplayTestCase(SubmitTestCase):
    def setUp(self):
        super(StudentDisplayTestCase, self).setUp()
        self.loginUser(self.enrolled_students[0])

    def createSubmissions(self):
        self.openAssignmentSub = self.createSubmission(self.current_user, self.openAssignment)
        self.softDeadlinePassedAssignmentSub = self.createSubmission(self.current_user, self.softDeadlinePassedAssignment)
        self.hardDeadlinePassedAssignmentSub = self.createSubmission(self.current_user, self.hardDeadlinePassedAssignment)

        self.submissions = (
            self.openAssignmentSub,
            self.softDeadlinePassedAssignmentSub,
            self.hardDeadlinePassedAssignmentSub,
        )

    def testCanSeeSubmissions(self):
        self.loginUser(self.enrolled_students[0])

        self.createSubmissions()
        cases = {
            self.openAssignmentSub: (200, ),
            self.softDeadlinePassedAssignmentSub: (200, ),
            self.hardDeadlinePassedAssignmentSub: (200, ),
        }
        for submission in cases:
            response = self.c.get('/details/%s/' % submission.pk)
            expected_responses = cases[submission]
            self.assertIn(response.status_code, expected_responses)

    def testCannotSeeOtherUsers(self):
        self.loginUser(self.enrolled_students[1])
        self.createSubmissions()

        self.loginUser(self.enrolled_students[0])
        cases = {
            self.openAssignmentSub: (403, ),
            self.softDeadlinePassedAssignmentSub: (403, ),
            self.hardDeadlinePassedAssignmentSub: (403, ),
        }
        for submission in cases:
            response = self.c.get('/details/%s/' % submission.pk)
            expected_responses = cases[submission]
            self.assertIn(response.status_code, expected_responses)

    def testIndexView(self):
        # User is already logged in, expecting dashboard redirect
        response=self.c.get('/')
        self.assertEquals(response.status_code, 302)

    def testIndexWithoutLoginView(self):
        self.c.logout()
        response=self.c.get('/')
        self.assertEquals(response.status_code, 200)

    def testLogoutView(self):
        # User is already logged in, expecting redirect
        response=self.c.get('/logout/')
        self.assertEquals(response.status_code, 302)

    def testNewSubmissionView(self):
        response=self.c.get('/assignments/%s/new/' % self.openAssignment.pk)
        self.assertEquals(response.status_code, 200)

    def testSettingsView(self):
        response=self.c.get('/settings/')
        self.assertEquals(response.status_code, 200)
        # Send new data, saving should redirect to dashboard
        response=self.c.post('/settings/',
            {'username':'foobar',
             'first_name': 'Foo',
             'last_name': 'Bar',
             'email': 'foo@bar.eu'}
        )
        self.assertEquals(response.status_code, 302)
        u = User.objects.get(pk=self.current_user.user.pk)
        self.assertEquals(u.username, 'foobar')

    def testCoursesView(self):
        response=self.c.get('/courses/')
        self.assertEquals(response.status_code, 200)

    def testChangeCoursesView(self):
        response=self.c.get('/courses/')
        self.assertEquals(response.status_code, 200)
        # Send new data, saving should redirect to dashboard
        course_ids = [str(self.course.pk), str(self.anotherCourse.pk)]
        response=self.c.post('/courses/', {u'courses': course_ids})
        self.assertEquals(response.status_code, 302)

    def testEnforcedUserSettingsView(self):
        self.current_user.user.first_name=""
        self.current_user.user.save()
        response=self.c.get('/dashboard/')
        self.assertEquals(response.status_code, 302)

    def testDashboardView(self):
        response=self.c.get('/dashboard/')
        self.assertEquals(response.status_code, 200)

    def testMachineView(self):
        self.createTestMachine('127.0.0.1')
        response=self.c.get('/machine/%u/'%self.machine.pk)
        self.assertEquals(response.status_code, 200)

    def testCannotUseTeacherBackend(self):
        response = self.c.get('/teacher/opensubmit/submission/')
        self.assertEquals(response.status_code, 302)        # 302: can access the model in principle, 403: can never access the app label

    def testCannotUseAdminBackend(self):
        response = self.c.get('/admin/auth/user/')
        #TODO: Still unclear why this is not raising 403 (see below)
        self.assertEquals(response.status_code, 302)        # 302: can access the model in principle, 403: can never access the app label

    def testStudentBecomesCourseOwner(self):
        # Before rights assignment        
        response = self.c.get('/teacher/opensubmit/course/%u/'%(self.course.pk))
        self.assertEquals(response.status_code, 302)        # 302: can access the model in principle, 403: can never access the app label
        # Assign rights
        old_owner = self.course.owner
        self.course.owner = self.current_user.user
        self.course.save()
        # After rights assignment
        response = self.c.get('/teacher/opensubmit/course/%u/'%(self.course.pk))
        self.assertEquals(response.status_code, 200)        
        # Take away rights
        self.course.owner = old_owner
        self.course.save()
        # After rights removal
        response = self.c.get('/teacher/opensubmit/course/%u/'%(self.course.pk))
        self.assertEquals(response.status_code, 302)        # 302: can access the model in principle, 403: can never access the app label

    def testCannotUseAdminBackendAsCourseOwner(self):
        # Assign rights
        self.course.owner = self.current_user.user
        self.course.save()
        # Admin access should be still forbidden
        response = self.c.get('/admin/auth/user/')
        self.assertEquals(response.status_code, 403)        # 302: can access the model in principle, 403: can never access the app label

    def testCannotUseAdminBackendAsTutor(self):
        # Assign rights
        self.course.tutors.add(self.current_user.user)
        self.course.save()
        # Admin access should be still forbidden
        response = self.c.get('/admin/auth/user/')
        self.assertEquals(response.status_code, 403)        # 302: can access the model in principle, 403: can never access the app label

    def testStudentBecomesTutor(self):
        # Before rights assignment
        response = self.c.get('/teacher/opensubmit/submission/')
        self.assertEquals(response.status_code, 302)        # 302: can access the model in principle, 403: can never access the app label
        # Assign rights
        self.course.tutors.add(self.current_user.user)
        self.course.save()
        # After rights assignment
        response = self.c.get('/teacher/opensubmit/submission/')
        self.assertEquals(response.status_code, 200)        # Access allowed
        # Take away rights
        self.course.tutors.remove(self.current_user.user)
        self.course.save()
        # After rights removal
        response = self.c.get('/teacher/opensubmit/submission/')
        self.assertEquals(response.status_code, 302)        # 302: can access the model in principle, 403: can never access the app label


