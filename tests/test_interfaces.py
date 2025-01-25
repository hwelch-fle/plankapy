import plankapy.interfaces as iface
import time


def test_interfaces(planka: iface.Planka):
    try:
        assert planka.me, "Failed to access authenticated user"

        # Create test user
        for user in planka.users:
            if user.name in ('testuser', 'testuser2'):
                user.delete()
        assert (test_user := planka.create_user(username="testuser", password='plAnkat3st', email='fake@email.com'))
        test_user2 = planka.create_user(username='testuser2', email='testuser2@email.com', password='lottaNumb3rs')
        time.sleep(1)

        # Project Tests
        assert (test_project := planka.create_project("Testing")), "Failed to create Project"
        assert test_project.set_background_gradient("algae-green") is None, "Failed to set Project Gradient"
        assert test_project.add_project_manager(test_user), "Failed to add project manager"
        assert test_project.remove_project_manager(test_user) is None, "Failed to remove project manager"
        assert test_project.add_project_manager(test_user.id), "Failed to add manager by id"

        time.sleep(1)

        # Board Tests
        assert (board := test_project.create_board("Test Board")), "Failed to create Board"
        assert (list1 := board.create_list("Test List 1")), "Failed to create List"
        list2 = board.create_list("Test List 2")
        assert (label1 := board.create_label("Test Label 1"))
        label2 = board.create_label("Test Label 2")
        assert board.add_user(test_user2)
        board.remove_user(test_user2)

        time.sleep(1)

        # Card Tests
        card = list1.create_card(name="Card 1")
        card_copy = card.duplicate()
        card_copy.move(list2)
        card.add_stopwatch()
        card_copy.add_stopwatch()
        card.add_label(label1)

        time.sleep(1)

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

        print("Interface Tests - Passed")
        return True

    finally:
        test_project.delete()
        test_user.delete()
        test_user2.delete()
    
    return False