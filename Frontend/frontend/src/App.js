import Index from './components/start/Index';
import SignIn from './components/start/SignIn';
import Dashboard from './components/dashboard/Index';
import Courses from './components/dashboard/home/Courses';
import Profile from './components/dashboard/profile/Profile'
import RequireAuth from './RequireAuth';
import {
  Route,
  Switch,
  BrowserRouter as Router
} from 'react-router-dom';

function App() {

  return (
    <Router>
      <Switch>
        <Route path='/courses' exact component={RequireAuth(Courses)} />
        <Route path='/dashboard/:id?' exact component={RequireAuth(Dashboard)} />
        <Route path='/login' exact component={SignIn} />
        <Route path='/' exact component={Index} />
        <Route path='/u/:slug' exact component={RequireAuth(Profile)} />
      </Switch>
    </Router>
  );
}

export default App;
