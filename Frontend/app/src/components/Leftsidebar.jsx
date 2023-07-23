import React from "react";

export default function Leftsidebar() {
  return (
    <>
      <div className="col-md-3">
        <div className="card">
          <div className="card-body">
            <div className="h5">Username</div>
            <div className="h7">School: University of Waterloo</div>
            <div className="h7">
              Profile description
            </div>
            <a href="#" className="card-link">
              Settings
            </a>
          </div>
          <ul className="list-group list-group-flush">
            <li className="list-group-item">
              <div className="h6">CLAS</div>
              <div className="h7">104</div>
              <div className="h6">ECE</div>
              <div className="h7">455</div>
              <div className="h7">458</div>
              <div className="h7">498A</div>
              <div className="h6">MSCI</div>
              <div className="h7">331</div>
            </li>
          </ul>
        </div>
      </div>
    </>
  );
}
