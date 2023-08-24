import Index from './components/start/Index';
import SignIn from './components/start/SignIn';
import Dashboard from './components/dashboard/Index';
import Courses from './components/dashboard/home/Courses';
import Profile from './components/dashboard/profile/Profile'
import {
  Route,
  Switch,
  BrowserRouter as Router
} from 'react-router-dom';

function App() {

  return (
    <Router>
      <Switch>
        <Route path='/courses' exact component={Courses} />
        <Route path='/dashboard' exact component={Dashboard} />
        <Route path='/login' exact component={SignIn} />
        <Route path='/' exact component={Index} />
        <Route path='/u/:slug' exact component={Profile} />
      </Switch>
    </Router>
  );
}

export default App;
