import React from 'react';
import Chat from './home/Chat';
import About from './home/About';

export default function RightSidebar() {
    return (
        <section className="rightsidebar">
            <About />
            <Chat />
        </section>
    )
}