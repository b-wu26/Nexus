import React from 'react';
import { useSelector } from 'react-redux';
import { Redirect } from 'react-router-dom';

const RequireAuth = (WrappedComponent) => {
  const AuthCheck = (props) => {
    const user = useSelector(state => state.user);
    
    if (Object.keys(user).length === 0) {
      return <Redirect to="/login" />;
    }

    return <WrappedComponent {...props} />;
  };

  return AuthCheck;
};

export default RequireAuth;