import { useEffect } from "react";
import { useSelector } from "react-redux";
import { Helmet } from "react-helmet";

import LeftSidebar from "./LeftSidebar";
import RightSidebar from "./RightSidebar";
import Navbar from "./Navbar";
import CreatePost from "./post/CreatePost";
import Posts from "./post/Posts";
import { addPost } from "../../redux/actions"


function Dashboard(props) {
    const user = useSelector((state) => state.user);
    // console.log("user_id in index.js");
    // console.log(user);
    const course_id = props.match.params.id;

    useEffect(() => {
        window.scrollTo(0, 0);
    }, [])

    return (
        <section className="dashboard">
            <Helmet>
                <title>Dashboard</title>
            </Helmet>
            <Navbar />
            <div className="navbar-spacer"></div>
            <div className="container">
                <div className="row">
                    <div className="col-lg-3 col-12">
                        <LeftSidebar active={1} />
                    </div>
                    <div className="col-lg-6 col-12 timeline">
                        <CreatePost course_id={course_id} />
                        <Posts course_id={course_id} />
                    </div>
                    <div className="col-lg-3 col-12">
                        <RightSidebar />
                    </div>
                </div>
            </div>
        </section>
    );
}

export default Dashboard;
