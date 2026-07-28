import json
from datetime import datetime

ASSIGNMENT_DATA = 'assignments.json'


def show_homepage(): 

    print('\n====================================')
    print('Homework Tracker by Mitchell Walker')
    print('====================================\n')
  
    print('Here you can organize your assignments and see what is due soon.')
    print('Information is stored locally on this device.')
    print()
    print('You are currently in the Main Menu:')
    print('1. View upcoming assignments')
    print('2. Add new assignment')
    print('3. View completed assignments')
    print('4. Mark assignment complete')
    print('5. Help')
    print('6. Exit')


# JSON functions 
def load_assignments():
    try:
        with open(ASSIGNMENT_DATA, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_assignments(assignments):
    with open(ASSIGNMENT_DATA, 'w') as file:
        json.dump(assignments, file, indent=4)



# Helper Functions
def add_assignment(assignments):
    """
      Stores formatted assignment details into assignments.json. 
      That is formatted in teh from of a dictionary data container
    """

    print()
    print('====================================')
    print('        ADD NEW ASSIGNMENT')
    print('====================================')
    print('Please enter the assignment title.')
    print('Enter 0 at any time to return to main menu.')
    print()

    # input title
    title = input('Assignment title: ').strip()
    if title == '0':
        print('Add assignment cancelled.')
        return
    print()

    # input course name
    print('Please enter the course name.')
    course = input('course name: ').strip()
    if course == '0':
        print('Add Assignment Cancelled.')
        return

 
    print('\nPlease enter the due date.')
    print('Using this format: MM-DD-YYYY')

    # validate the input date
    while True:
        due_date = input('Due date: ').strip()

        if due_date == '0':
            print('Add assignment cancelled.')
            return

        try:
            datetime.strptime(due_date, '%m-%d-%Y')
            break
        except ValueError:
            print('Invalid date format.')
            print('Please try again using MM-DD-YYYY, like 08-29-2015.')
            print('Or enter 0 to return to the main menu')

    print()
    print('Assignment has been added with the following description:')
    print(f'Title: {title}')
    print(f'Course: {course}')
    print(f'Due date: {due_date}')
    print()

    confirm = input('Save this assignment? (Y/N):').strip().lower()

    # Formatted text will appear in assignments.json, Completed attribute will be set to False innately
    if confirm == 'y':
        new_assignment = {
            'title': title,
            'course': course,
            'due_date': due_date,
            'completed': False
        }
        assignments.append(new_assignment)
        save_assignments(assignments)

        print('Assignment saved successfully!')
    else:
        print('Assignment was not saved')



def view_assignments(assignments):
    """ """

    print()
    print('====================================')
    print('     UPCOMING ASSIGNMENTS')
    print('====================================')

    upcoming = []

    # don't display completed(True) assignments
    for assignment in assignments:
        if assignment["completed"] == False:
            upcoming.append(assignment)

    if len(upcoming) == 0:
        print('No upcoming assignments found.')
        return

    # Sort current assignments by due date
    upcoming.sort(key = lambda assignment: assignment['due_date'])

    for index, assignment in enumerate(upcoming, start=1):
        print(f"Assignment: {index}. {assignment['title']}")
        print(f"   Course: {assignment['course']}")
        print(f"   Due date: {assignment['due_date']}")
        print()


def view_completed_assignments(assignments):
    """ """

    print()
    print('====================================')
    print('     COMPLETED ASSIGNMENTS')
    print('====================================')

    completed_list = []
    
    # Only display completed assignments
    for assignment in assignments:
        if assignment['completed'] == True:
            completed_list.append(assignment)

    if len(completed_list) == 0:
        print('No completed assignments found.')
        return

    # Display completed assignments
    for index, assignment in enumerate(completed_list, start=1):
        print(f"{index}. {assignment['title']}")
        print(f"   Course: {assignment['course']}")
        print(f"   Due date: {assignment['due_date']}")
        print()



def mark_assignment_complete(assignments):
    print()
    print('====================================')
    print('    MARK ASSIGNMENT COMPLETE')
    print('====================================')

    print('Choose an assignment to mark as completed:')
    print('Type 0 to cancel and return to the main menu.')
    print()

    # This list connects the displayed numbers back to the real assignments
    assignment_indexes = []
    display_number = 1

    for index in range(len(assignments)):
        assignment = assignments[index]

        # Displays uncompleted assignments 
        if assignment['completed'] == False:
            print(f'{display_number}. {assignment['title']}')
            print(f'   Course: {assignment['course']}')
            print(f'   Due date: {assignment['due_date']}')
            print()

            assignment_indexes.append(index)
            display_number += 1

    if len(assignment_indexes) == 0:
        print('No incomplete assignments to mark completed')
        return

    choice = input('Assignment number: ')

    if choice == '0':
        print('Cancelled. No assignment was changed.')
        return

    if choice.isdigit() == False:
        print('Invalid input. Please enter a number.')
        return

    choice_number = int(choice)

    if choice_number < 1 or choice_number > len(assignment_indexes):
        print('Invalid assignment number.')
        return

    # converts choice back into the original list index
    real_index = assignment_indexes[choice_number - 1]
    selected_assignment = assignments[real_index]

    print()
    print('You selected: ')
    print(f"{selected_assignment['title']} - {selected_assignment['course']} - due {selected_assignment['due_date']}")
    print()
    print('This will mark the assignment as complete.')

    #  confirms if you want to mark assignment as Completed(False to True)
    confirm = input('Continue? (Y/N): ').strip().lower()

    # save the change
    if confirm == 'y':
        assignments[real_index]['completed'] = True
        save_assignments(assignments)
        print('Assignment marked complete, well done!')
    else:
        print('No changes were made. ')



#     =========== MAIN =============
def main():

    assignments = load_assignments()

    while True:
        show_homepage()

        choice = input('\nPlease choose a menu option: ')

        if choice == '1':
            print('\nView upcoming assignments selected')
            view_assignments(assignments)

        elif choice == '2':
            print('\nAdd assignment selected')
            add_assignment(assignments)

        elif choice == '3':
            print('\nView completed assignments selected')
            view_completed_assignments(assignments)

        elif choice == '4':
            print('\nMark assignment complete selected.')
            mark_assignment_complete(assignments)

        elif choice == '5':
            print('Help selected.')

        elif choice == '6':
            print('Thankyou, goodbye')
            break
        else:
            print('Choice is invalid, please choose a number from 1 to 6.')

        input('\nPress Enter to return to the Main Menu: ')


main()