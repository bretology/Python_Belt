from system.core.controller import *

class Pokes(Controller):
    def __init__(self, action):
        super(Pokes, self).__init__(action)
        
        self.load_model('Poke')
        self.db = self._app.db
    
    def all_pokes(self):
        if 'id' in session:
            poked_you_num = self.models['Poke'].load_num_people(session['id'])
            poked_you_people = self.models['Poke'].load_people(session['id'])
            all_people_pokes = self.models['Poke'].load_all_pokes(session['id'])
            poked_you_num = len(poked_you_people)
            print poked_you_people
            return self.load_view('pokes.html', all = all_people_pokes, persons = poked_you_num, listed = poked_you_people)
        else:
            return redirect('/')

    def add_poke(self, id):
        self.models['Poke'].poke_someone(session['id'], id)
        return redirect('/pokes')