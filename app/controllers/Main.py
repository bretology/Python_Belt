from system.core.controller import *

class Main(Controller):
    def __init__(self, action):
        super(Main, self).__init__(action)
        
        self.load_model('Poke')
        self.db = self._app.db
   
    def index(self):
        if 'id' in session:
            return redirect('/pokes')
        else:
            return self.load_view('index.html')

    def register(self):
        register_status = self.models['Poke'].create_user(request.form)
        if register_status['valid']:
            session['id'] = register_status['user']['id']
            session['alias'] = register_status['user']['alias']
            return redirect('/pokes')
        else:
            for error in register_status['errors']:
                flash(error)
            return redirect('/')

    def login(self):
        login_status = self.models['Poke'].login_user(request.form)
        if login_status['valid']:
            session['id'] = login_status['user']['id']
            session['alias'] = login_status['user']['alias']
            return redirect('/pokes')
        else:
            for error in login_status['errors']:
                flash(error)
            return redirect('/')

    def logout(self):
        session.clear()
        return redirect('/')

