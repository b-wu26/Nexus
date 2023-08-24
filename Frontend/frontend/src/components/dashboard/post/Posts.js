import React, { useEffect} from 'react';
import axios from 'axios';
import TimelinePost from './TimelinePost';
import { useDispatch, useSelector } from 'react-redux';
import { setPosts } from "../../../redux/actions"
import { BACKEND_SERVER_DOMAIN } from '../../../settings'

function Posts() {
    const posts = [{id: 0,
                    poster: {first: "some", last: "one"},
                    pfp: "https://hips.hearstapps.com/hmg-prod/images/index-oppenheimer-1659022637.jpg?crop=0.502xw:1.00xh;0.250xw,0&resize=1200:*",
                    created: "10 mins ago",
                    post_text: "lorem ipsum saijdh oisajdoi sahd iusaghdi uhsauo dhasuidhoa"},
                    {id: 1,
                    poster: {first: "some", last: "body"},
                    pfp: "https://www.byrdie.com/thmb/EARorYOqSQX2EJkikXP01WpjalU=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/kentanrecirc-587700af52e748ca982715c6cd95b65e.png",
                    created: "1 week ago",
                    post_text: "the quick brown fox jumps over the lazy dog",
                    post_image: "https://upload.wikimedia.org/wikipedia/en/4/4b/Jjportrait.jpg"}];
    return (
        <section className="timeline-posts">
            {posts.map((post) => (
                <TimelinePost post={post}/>
            ))}
        </section>
    );
}

export default Posts;