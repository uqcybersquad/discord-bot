import requests
from bs4 import BeautifulSoup


class UQScraper:
    """
    Scrapes course data from my.uq.edu website.

    Removed caching since monkey patching was done
    on run.py

    params: course code ex: COMP3320
    """

    def __init__(self, course_code: str):
        # user-agent required else UQ aborts connection
        headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        }

        self.url = (
            "http://my.uq.edu.au/programs-courses/course.html?course_code={}".format(
                course_code
            )
        )
        r = requests.get(self.url, headers=headers)
        self.soup = BeautifulSoup(r.content, "html.parser")

        # Check for error from UQ response
        err = self.soup.select_one(".elementErrorList")
        if err is not None:
            raise ValueError(err.text.strip())

    def get_url(self):
        """
        Returns url of course profile
        """
        return self.url

    def get_title(self):
        """
        Obtains the course title
        Silently ignores and passes a blank str if title can't be found.
        returns: course title
        """
        course_title = self.soup.select_one("#course-title")
        if course_title is None:
            return "?"
        return course_title.text.strip()

    def get_level(self):
        """
        Obtains the course level (eg: Undergraduate, Masters).
        Silently ignores and passes a blank str if level can't be found.
        returns: course level
        """
        course_level = self.soup.select_one("#course-level")
        if course_level is None:
            return "?"
        return course_level.text.strip()

    def get_faculty(self):
        """
        Obtains the faculty.
        Silently ignores and passes a blank str if faculty can't be found.
        returns: course faculty
        """
        course_faculty = self.soup.select_one("#course-faculty")
        if course_faculty is None:
            return "?"
        return course_faculty.text.strip()

    def get_school(self):
        """
        Obtains the school in charge to the course.
        Silently ignores and passes a blank str if school can't be found.
        returns: course school
        """
        course_school = self.soup.select_one("#course-school")
        if course_school is None:
            return "?"
        return course_school.text.strip()

    def get_units(self):
        """
        Obtains the course's no. of units.
        Silently ignores and passes a blank str if units can't be found.
        returns: course units
        """
        course_units = self.soup.select_one("#course-units")
        if course_units is None:
            return "?"
        return course_units.text.strip()

    def get_duration(self):
        """
        Obtains the course's duration.
        Silently ignores and passes a blank str if duration can't be found.
        returns: course duration
        """
        course_duration = self.soup.select_one("#course-duration")
        if course_duration is None:
            return "?"
        return course_duration.text.strip()

    def get_contact(self):
        """
        Obtains the course's contact hours.
        Silently ignores and passes a blank str if contact can't be found.
        returns: course contact
        """
        course_contact = self.soup.select_one("#course-contact")
        if course_contact is None:
            return "?"
        return course_contact.text.strip()

    def get_prerequisite(self):
        """
        Obtains the course's prerequisite.
        Silently ignores and passes a blank str if prerequisite can't be found.
        returns: course prerequisite
        """
        course_prerequisite = self.soup.select_one("#course-prerequisite")
        if course_prerequisite is None:
            return "?"
        return course_prerequisite.text.strip()

    def get_companion(self):
        """
        Obtains the course's companion.
        Silently ignores and passes a blank str if companion can't be found.
        returns: course companion
        """
        course_companion = self.soup.select_one("#course-companion")
        if course_companion is None:
            return "?"
        return course_companion.text.strip()

    def get_recommended_prerequisite(self):
        """
        Obtains the course's recommended prerequisite.
        Silently ignores and passes a blank str if recommended prerequisites can't be found.
        returns: course recommended-prerequisite
        """
        course_recommended_prerequisite = self.soup.select_one(
            "#course-recommended-prerequisite"
        )
        if course_recommended_prerequisite is None:
            return "?"
        return course_recommended_prerequisite.text.strip()

    def get_assessment(self):
        """
        Obtains the course's assessment methods.
        Silently ignores and passes a blank str if assessments can't be found.
        returns: course assessment-methods
        """
        course_assessment_methods = self.soup.select_one("#course-assessment-methods")
        if course_assessment_methods is None:
            return "?"
        return course_assessment_methods.text.strip()

    def get_coordinator(self):
        """
        Obtains the course's coordinator
        Silently ignores and passes a blank str if coordinator can't be found.
        returns: course coordinator
        """
        course_coordinator = self.soup.select_one("#course-coordinator")
        if course_coordinator is None:
            return "?"
        return course_coordinator.text.strip()

    def get_summary(self):
        """
        Obtains the course's summary
        Silently ignores and passes a blank str if summary can't be found.
        returns: course summary
        """
        course_summary = self.soup.select_one("#course-summary")
        if course_summary is None:
            return "?"
        return course_summary.text.strip()


# Test driver
# scraper = UQScraper("COMP3320")
# print(scraper.get_recommended_prerequisite())
