from flask import Flask, render_template, request, redirect, url_for

from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

class Person:
    def __init__(self, id, name, contact):
        self.id = id
        self.name = name
        self.contact = contact
        self.tickets_assigned = []

people = [
    Person("1", "John", "123-456-7890"),
    Person("2", "Alice", "987-654-3210"),
    Person("3", "Bob", "555-555-5555"),
    Person("4", "Emma", "111-222-3333"),
    Person("5", "David", "444-444-4444")
]

tickets = []
current_person_index = 0



@app.route('/')
def index():
    total_tickets_assigned = sum(len(person.tickets_assigned) for person in people)
    return render_template('index.html', people=people, total_tickets_assigned=total_tickets_assigned)




@app.route('/assign_ticket', methods=['GET', 'POST'])
def assign_ticket():
    global current_person_index
    if request.method == 'POST':
        if current_person_index >= len(people):
            current_person_index = 0

        person = people[current_person_index]
        current_person_index = (current_person_index + 1) % len(people)

        issue_description = request.form['issue_description']
        raised_by_id = request.form['raised_by'] 

        raised_by = next((p for p in people if p.id == raised_by_id), None) 

        if raised_by:
            ticket = {"id": len(tickets) + 1, "issue_description": issue_description, "assigned_to": person, "raised_by": raised_by}
            person.tickets_assigned.append(ticket)
            tickets.append(ticket)

    return render_template('assign_ticket.html', people=people)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        contact = request.form['contact']
        new_id = str(len(people) + 1)
        new_person = Person(new_id, name, contact)
        people.append(new_person)
    return render_template('add_user.html')

@app.route('/delete_user/<string:id>', methods=['POST'])
def delete_user(id):
    global people
    people = [person for person in people if person.id != id]
    return redirect(url_for('index'))


@app.route('/tickets')
def ticket_list():
    return render_template('ticket_list.html', tickets=tickets)

@app.route('/available_users')
def available_users():
    available_users = [{'id': person.id, 'name': person.name} for person in people]
    return jsonify(available_users)
if __name__ == '__main__':
    app.run()
