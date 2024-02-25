import React, { useState, useRef } from "react";
import logo from "../../assets/images/logo.png";
import InputField from "../../utils/InputField";
import { Helmet } from "react-helmet";
import axios from "axios";
import { useDispatch } from "react-redux";
import { useSelector } from "react-redux";
import { setUser } from "../../redux/actions";
import { useHistory } from "react-router-dom";
import { BACKEND_SERVER_DOMAIN } from "../../settings";
import { Link } from "react-router-dom";
import {themeApply} from '../global/ThemeApply'

export default function SignIn() {
    const dispatch = useDispatch();
    const history = useHistory();
    const userState = useSelector((state) => state.user);

    themeApply();
    
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [apiResponse, setAPIResponse] = useState();

    const handleEmail = ({ target }) => {
        setEmail(target.value);
    };
    const handlePassword = ({ target }) => {
        setPassword(target.value);
    };
    let btnRef = useRef();

    const handleLogIn = () => {

        if (!email || !password) {
            setAPIResponse(
                <div className="fw-bold text-danger text-sm pb-2">
                    Missing email or password.
                </div>);
            return;
        }

        if (btnRef.current) {
            btnRef.current.setAttribute("disabled", "disabled");
        }
        let config = {
            headers: {
                "Content-Type": "multipart/form-data",
            },
        };
        const loginRequest = new FormData();
        loginRequest.append("email", email);
        loginRequest.append("password", password); 
        axios
            .post(
                `${BACKEND_SERVER_DOMAIN}/api/user/login`,
                loginRequest,
                config
            )
            .then(function (response) {
                    if (response.status === 200) {
                    dispatch(setUser(response.data["user"]));
                    history.push("/dashboard");
                }
            })
            .catch(function (error) {
                console.log(error) 
                setAPIResponse(
                    <div className="fw-bold text-danger text-sm pb-2">
                        Unable to sign in, make sure your email and password are correct.
                    </div>
                );
                if (btnRef.current) {
                    btnRef.current.removeAttribute("disabled");
                }
            });
    };

    return (
        <section className="login bg-social-icons">
            <Helmet>
                <title>Sign in to Nexus</title>
            </Helmet>
            <div className="container">
                <div className="col-lg-5 col-md-12 col-sm-12">
                    <div className="d-flex align-content-center justify-content-center"> 
                        <img src={logo} className="logo"/>
                    </div>
                    {
                        <div className="card">
                            <h3>Sign in</h3>
                            {apiResponse}
                            <InputField
                                label="Email"
                                onChange={handleEmail}
                                name="email"
                                type="email"
                            />
                            <InputField
                                label="Password"
                                onChange={handlePassword}
                                name="password"
                                type="password"
                            />
                            <button
                                type="submit"
                                ref={btnRef}
                                onClick={handleLogIn}
                                className="btn btn-primary btn-main"
                            >
                                Sign in
                            </button>
                            <span>
                                <Link to="#">Reset Password</Link>{" "}
                                or <Link to="/">Sign Up</Link>
                            </span>
                        </div>
                    }
                </div>
            </div>
        </section>
    );
}
