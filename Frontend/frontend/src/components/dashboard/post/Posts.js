import React, { useEffect, useState } from 'react';
import axios from 'axios';
import TimelinePost from './TimelinePost';
import { useDispatch, useSelector } from 'react-redux';
import { setPosts } from "../../../redux/actions"
import { BACKEND_SERVER_DOMAIN } from '../../../settings'


function Posts(props) {
    const [posts, setPosts] = useState([]); // initialize posts state
    const user = useSelector((state) => state.user); // Replace with your actual user ID
    const user_id = user.idstudent_profile;

    console.log("user_id");
    console.log(user_id);
    useEffect(() => {
        if (props.course_id) {
            axios.get(`${BACKEND_SERVER_DOMAIN}/api/feed/${user_id}/${props.course_id}`)
                .then((response) => {
                    console.log(response);
                    setPosts(response.data);
                })
                .catch((error) => {
                    console.error(`Error fetching data: ${error}`);
                });
        } else {
            axios.get(`${BACKEND_SERVER_DOMAIN}/api/feed/${user_id}`)
                .then((response) => {

                    console.log("response from backend");
                    console.log(response);
                    setPosts(response.data);
                })
                .catch((error) => {
                    console.error(`Error fetching data: ${error}`);
                });
        }
    }, []); // empty dependency array means this effect will only run once (like componentDidMount in classes)

    console.log(posts);
    return (
        <section className="timeline-posts">
            {posts.map((post) => (
                <TimelinePost post={post} />
            ))}
        </section>
    );
}

export default Posts;