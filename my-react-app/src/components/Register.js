import React from 'react';

const Register = () => {
  return (
    <div>
      <h1>Registration Page</h1>
      <form>
        <label>
          Username:
          <input type="text" name="username" />
        </label>
        <label>
          Password:
          <input type="password" name="password" />
        </label>
        <input type="submit" value="Register" />
      </form>
    </div>
  );
};

export default Register;
