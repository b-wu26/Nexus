import React from "react";
import Leftsidebar from "./Leftsidebar";
import Content from "./Content";
import Rightsidebar from "./Rightsidebar";
import Navbar from "./Navbar";

export default function HomePage() {
  return (
    <>
      <Navbar />
      <div className="container-fluid gedf-wrapper">
        <div className="row">
          <Leftsidebar />
          <Content />
          <Rightsidebar />
        </div>
      </div>
    </>
  );
}