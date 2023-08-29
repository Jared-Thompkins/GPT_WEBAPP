import React, { useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';

const Index = () => {
    const { user } = useAuth();
  
    useEffect(() => {
      console.log('User in Index:', user);
    }, [user]);
  
    return (
      <div>
        <h1>Home Page</h1>
        {user ? <p>Welcome, {user.username}!</p> : <p>You are not logged in.</p>}
      </div>
    );
  };

export default Index;