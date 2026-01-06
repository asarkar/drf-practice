from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Answer, Category, Question, Quiz


class QuizListViewTests(APITestCase):
    """Tests for QuizListView."""

    category: Category
    url: str

    def setUp(self) -> None:
        self.category = Category.objects.create(name="Programming")
        self.url = reverse("quizzes:quiz-list")

    def test_list_quizzes_empty(self) -> None:
        """Test listing quizzes when none exist."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_list_quizzes_single(self) -> None:
        """Test listing quizzes with a single quiz."""
        Quiz.objects.create(title="Python Basics", category=self.category)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Python Basics")

    def test_list_quizzes_multiple(self) -> None:
        """Test listing quizzes with multiple quizzes."""
        Quiz.objects.create(title="Python Basics", category=self.category)
        Quiz.objects.create(title="Django Advanced", category=self.category)
        Quiz.objects.create(title="REST API Design", category=self.category)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        titles = [quiz["title"] for quiz in response.data]
        self.assertIn("Python Basics", titles)
        self.assertIn("Django Advanced", titles)
        self.assertIn("REST API Design", titles)

    def test_list_quizzes_returns_only_title(self) -> None:
        """Test that serializer returns only the title field."""
        Quiz.objects.create(title="Test Quiz", category=self.category)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(list(response.data[0].keys()), ["title"])


class RandomQuestionViewTests(APITestCase):
    """Tests for RandomQuestionView."""

    category: Category
    quiz: Quiz
    question: Question
    answer1: Answer
    answer2: Answer

    def setUp(self) -> None:
        self.category = Category.objects.create(name="Programming")
        self.quiz = Quiz.objects.create(title="Python", category=self.category)
        self.question = Question.objects.create(
            quiz=self.quiz,
            title="What is a list comprehension?",
            difficulty=1,
        )
        self.answer1 = Answer.objects.create(
            question=self.question,
            answer_text="A concise way to create lists",
            is_right=True,
        )
        self.answer2 = Answer.objects.create(
            question=self.question,
            answer_text="A type of loop",
            is_right=False,
        )

    def get_url(self, topic: str) -> str:
        return reverse("quizzes:question-random", kwargs={"topic": topic})

    def test_get_random_question_success(self) -> None:
        """Test getting a random question for an existing topic."""
        response = self.client.get(self.get_url("Python"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("title", response.data)
        self.assertIn("answers", response.data)

    def test_get_random_question_returns_correct_structure(self) -> None:
        """Test that random question has correct response structure."""
        response = self.client.get(self.get_url("Python"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "What is a list comprehension?")
        self.assertEqual(len(response.data["answers"]), 2)

    def test_get_random_question_includes_answer_details(self) -> None:
        """Test that answers include id, answer_text, and is_right."""
        response = self.client.get(self.get_url("Python"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        answer = response.data["answers"][0]
        self.assertIn("id", answer)
        self.assertIn("answer_text", answer)
        self.assertIn("is_right", answer)

    def test_get_random_question_nonexistent_topic(self) -> None:
        """Test getting a random question for a non-existent topic returns 404."""
        response = self.client.get(self.get_url("NonExistentTopic"))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_random_question_empty_topic(self) -> None:
        """Test getting a random question for a topic with no questions."""
        Quiz.objects.create(title="EmptyQuiz", category=self.category)

        response = self.client.get(self.get_url("EmptyQuiz"))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_random_question_case_sensitive(self) -> None:
        """Test that topic matching is case-sensitive."""
        response = self.client.get(self.get_url("python"))  # lowercase

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_random_question_multiple_questions(self) -> None:
        """Test that random question returns one of the available questions."""
        Question.objects.create(
            quiz=self.quiz,
            title="What is a dictionary?",
            difficulty=1,
        )
        Question.objects.create(
            quiz=self.quiz,
            title="What is a tuple?",
            difficulty=1,
        )

        valid_titles = {
            "What is a list comprehension?",
            "What is a dictionary?",
            "What is a tuple?",
        }

        response = self.client.get(self.get_url("Python"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(response.data["title"], valid_titles)


class QuizQuestionListViewTests(APITestCase):
    """Tests for QuizQuestionListView."""

    category: Category
    quiz: Quiz

    def setUp(self) -> None:
        self.category = Category.objects.create(name="Programming")
        self.quiz = Quiz.objects.create(title="Django", category=self.category)

    def get_url(self, topic: str) -> str:
        return reverse("quizzes:question-list", kwargs={"topic": topic})

    def test_get_questions_empty_topic(self) -> None:
        """Test getting questions for a topic with no questions."""
        response = self.client.get(self.get_url("Django"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_get_questions_nonexistent_topic(self) -> None:
        """Test getting questions for a non-existent topic returns empty list."""
        response = self.client.get(self.get_url("NonExistentTopic"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_get_questions_single_question(self) -> None:
        """Test getting questions when topic has one question."""
        question = Question.objects.create(
            quiz=self.quiz,
            title="What is Django?",
            difficulty=0,
        )
        Answer.objects.create(
            question=question,
            answer_text="A web framework",
            is_right=True,
        )

        response = self.client.get(self.get_url("Django"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "What is Django?")

    def test_get_questions_multiple_questions(self) -> None:
        """Test getting questions when topic has multiple questions."""
        Question.objects.create(quiz=self.quiz, title="What is Django?", difficulty=0)
        Question.objects.create(quiz=self.quiz, title="What is a model?", difficulty=1)
        Question.objects.create(quiz=self.quiz, title="What is a view?", difficulty=1)

        response = self.client.get(self.get_url("Django"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_get_questions_includes_quiz_info(self) -> None:
        """Test that questions include nested quiz information."""
        Question.objects.create(quiz=self.quiz, title="What is Django?", difficulty=0)

        response = self.client.get(self.get_url("Django"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("quiz", response.data[0])
        self.assertEqual(response.data[0]["quiz"]["title"], "Django")

    def test_get_questions_includes_answers(self) -> None:
        """Test that questions include nested answer information."""
        question = Question.objects.create(
            quiz=self.quiz,
            title="What is Django?",
            difficulty=0,
        )
        Answer.objects.create(
            question=question,
            answer_text="A web framework",
            is_right=True,
        )
        Answer.objects.create(
            question=question,
            answer_text="A database",
            is_right=False,
        )

        response = self.client.get(self.get_url("Django"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data[0]["answers"]), 2)

    def test_get_questions_answer_structure(self) -> None:
        """Test that answers have correct structure."""
        question = Question.objects.create(
            quiz=self.quiz,
            title="What is Django?",
            difficulty=0,
        )
        Answer.objects.create(
            question=question,
            answer_text="A web framework",
            is_right=True,
        )

        response = self.client.get(self.get_url("Django"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        answer = response.data[0]["answers"][0]
        self.assertIn("id", answer)
        self.assertIn("answer_text", answer)
        self.assertIn("is_right", answer)

    def test_get_questions_case_sensitive(self) -> None:
        """Test that topic matching is case-sensitive."""
        Question.objects.create(quiz=self.quiz, title="What is Django?", difficulty=0)

        response = self.client.get(self.get_url("django"))  # lowercase

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_get_questions_ordered_by_id(self) -> None:
        """Test that questions are returned ordered by id."""
        Question.objects.create(quiz=self.quiz, title="First question", difficulty=0)
        Question.objects.create(quiz=self.quiz, title="Second question", difficulty=1)
        Question.objects.create(quiz=self.quiz, title="Third question", difficulty=2)

        response = self.client.get(self.get_url("Django"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "First question")
        self.assertEqual(response.data[1]["title"], "Second question")
        self.assertEqual(response.data[2]["title"], "Third question")
