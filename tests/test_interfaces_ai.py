import pytest
import time

from plankapy import Planka, PasswordAuth

class TestInterfaceTests:

    @pytest.fixture
    def planka(self):
        # Setup code to initialize a Planka instance
        return Planka('http://localhost:3000', PasswordAuth('demo', 'demo'))

    def test_authenticated_user(self, planka: Planka):
        assert planka.me, "Failed to access authenticated user"

    def test_create_test_user(self, planka: Planka):
        for user in planka.users:
            if user.name in ('testuser', 'testuser2'):
                user.delete()
        test_user = planka.create_user(username="testuser", password='plAnkat3st', email='fake@email.com')
        assert test_user
        test_user2 = planka.create_user(username='testuser2', email='testuser2@email.com', password='lottaNumb3rs')
        assert test_user2

    def test_project_operations(self, planka: Planka):
        test_user = planka.create_user(username="testuser", password='plAnkat3st', email='fake@email.com')
        test_project = planka.create_project("Testing")
        assert test_project, "Failed to create Project"
        assert test_project.set_background_gradient("algae-green") is None, "Failed to set Project Gradient"
        assert test_project.add_project_manager(test_user), "Failed to add project manager"
        assert test_project.remove_project_manager(test_user) is None, "Failed to remove project manager"
        assert test_project.add_project_manager(test_user.id), "Failed to add manager by id"

    def test_board_operations(self, planka: Planka):
        test_user = planka.create_user(username="testuser", password='plAnkat3st', email='fake@email.com')
        test_project = planka.create_project("Testing")
        board = test_project.create_board("Test Board")
        assert board, "Failed to create Board"
        list1 = board.create_list("Test List 1")
        assert list1, "Failed to create List"
        list2 = board.create_list("Test List 2")
        label1 = board.create_label("Test Label 1")
        assert label1
        label2 = board.create_label("Test Label 2")
        assert board.add_user(test_user)
        board.remove_user(test_user)

    def test_card_operations(self, planka: Planka):
        test_user = planka.create_user(username="testuser", password='plAnkat3st', email='fake@email.com')
        test_project = planka.create_project("Testing")
        board = test_project.create_board("Test Board")
        list1 = board.create_list("Test List 1")
        list2 = board.create_list("Test List 2")
        label1 = board.create_label("Test Label 1")
        label2 = board.create_label("Test Label 2")
        card = list1.create_card(name="Card 1")
        card_copy = card.duplicate()
        card_copy.move(list2)
        card.add_stopwatch()
        card_copy.add_stopwatch()
        card.add_label(label1)
        card.remove_label(label1)
        card.stopwatch.set(hours=1)
        card.move(list2)
        card_copy.add_label(label2)
        card_copy.move(list1)
        card.add_comment("Hello World")

        with card_copy.editor():
            card_copy.name = "New Card"

        card_copy.stopwatch.start()
        time.sleep(2)
        card_copy.stopwatch.stop()
        assert card_copy.stopwatch.total == 2, "Stopwatch timer testing failed"