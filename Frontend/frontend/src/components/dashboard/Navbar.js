import React from "react";
import { logoutUser, removeAllPosts } from "../../redux/actions";
import logo from "../../assets/images/logo-no-text.png";
import { useSelector, useDispatch } from "react-redux";
import { Link, useHistory } from "react-router-dom";
import axios from "axios";
import { BACKEND_SERVER_DOMAIN } from "../../settings";
import { timeSince } from "../../utils/timesince";
import ThemeToggle from "../global/ThemeToggle";
import _ from 'lodash'

export default function Navbar() {
    const user = useSelector((state) => state.user);
    const [searchResults, setSearchResults] = React.useState(null);
    const dispatch = useDispatch();
    const history = useHistory();

    const logOut = () => {
        dispatch(logoutUser());
        dispatch(removeAllPosts());
        history.push("/login");
    };

    return (
        <nav className="navbar navbar-expand-lg navbar-light">
            <div className="container">
                <div className="container-fluid row">
                    <div className="col-lg-3 col-12 nav-brand">
                        <h6>
                            <img src={logo} />
                        </h6>
                        <button
                            className="navbar-toggler"
                            type="button"
                            data-bs-toggle="collapse"
                            data-bs-target="#navbarToggler"
                            data-toggle="collapse"
                            data-target="#navbarToggler"
                            aria-controls="navbarToggler"
                            aria-expanded="false"
                            aria-label="Toggle navigation"
                        >
                            <i className="fas fa-bars"></i>
                        </button>
                    </div>
                    <div className="col-lg-9 col-12">
                        <div
                            className="collapse navbar-collapse"
                            id="navbarToggler"
                        >
                            <div className="row w-100">
                                <div className="col-lg-8 col-12">
                                    {/* <form className="d-flex">
                                        <input
                                            type="search"
                                            placeholder="Search"
                                            aria-label="Search"
                                        />
                                        <button type="submit" disabled="disabled">
                                            <i className="fas fa-search"></i>
                                        </button>
                                    </form> */}
                                </div>
                                <div className="col-lg-4 col-12">
                                    <ul className="navbar-nav">
                                        <li className="d-md-block d-lg-none">
                                            <Link to={"/dashboard"}>
                                                <i className="far fa-newspaper"></i>
                                                &nbsp;&nbsp;&nbsp; Feed
                                            </Link>
                                        </li>
                                        <li className="d-md-block d-lg-none">
                                            <Link to={"/friends"}>
                                                <i className="fas fa-user-friends"></i>
                                                &nbsp;&nbsp;&nbsp; Friends
                                            </Link>
                                        </li>
                                        <li className="d-md-block d-lg-none">
                                            <Link to={"/u/" + user.slug}>
                                                <i className="far fa-user"></i>
                                                &nbsp;&nbsp;&nbsp; Profile
                                            </Link>
                                        </li>
                                        <li className="align-end">
                                            <div className="nav-theme-toggler">
                                                <ThemeToggle />
                                            </div>
                                            <button onClick={logOut}>
                                                <i className="fas fa-sign-out-alt"></i>
                                            </button>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </nav>
    );
}
