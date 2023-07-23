import React from "react";
import { useState } from "react";

const initialValuesRegister = {
  firstName: "",
  lastName: "",
  email: "",
  password: "",
  location: "",
  occupation: "",
  picture: "",
};

const initialValuesLogin = {
  email: "",
  password: "",
};

export default function Form() {

    return (
      <div className="login-form">
        <div>
        <input
          type="text"
          className="username-input"
          id="username"
          placeholder="Username"
        />
        </div>
        <div>
        <input
          type="text"
          className="password-input"
          id="password"
          placeholder="Password"
        />
        </div>
        <div>
        <button type="submit" className="btn btn-primary">
          Sign in
        </button>
        </div>
        <div>
        <div>
          <a href="#" className="card-link">
            Register
          </a>
          </div>
        </div>
      </div>
    );
};