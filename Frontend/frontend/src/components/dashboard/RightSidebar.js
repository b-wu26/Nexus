import React from 'react';
import Chat from './home/Chat';
import About from './home/About';

export default function RightSidebar(props) {
    console.log("Right side bar", props.course_id)

    return (
        <section className="rightsidebar">
            <About course_id={props.course_id} />
            <Chat course_id={props.course_id} />
        </section>
    )
}