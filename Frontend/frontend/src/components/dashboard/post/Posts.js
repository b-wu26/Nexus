import React, { useEffect, useState } from 'react';
import axios from 'axios';
import TimelinePost from './TimelinePost';
import { useDispatch, useSelector } from 'react-redux';
import { setPosts } from "../../../redux/actions"
import { BACKEND_SERVER_DOMAIN } from '../../../settings'

function Posts() {
    const [posts, setPosts] = useState([]); // initialize posts state

    useEffect(() => {
        axios.get(`${BACKEND_SERVER_DOMAIN}/api/feed/1`) // replace 'endpoint' with your actual endpoint
            .then((response) => {
                console.log(response);
                setPosts(response.data); // update posts state with the data from the response
            })
            .catch((error) => {
                console.error(`Error fetching data: ${error}`);
            });
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