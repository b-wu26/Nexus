import React from "react";

export default function Rightsidebar() {
  return (
    <>
      <div className="col-md-3">
        <div className="card gedf-card">
          <div className="card-body">
            <h5 className="card-title">ECE 498A</h5>
            <h6 className="card-subtitle mb-2 text-muted">Course description</h6>
            <p className="card-text">
              something something
            </p>
            <a href="#" className="card-link">
              Uwflow
            </a>
            <a href="#" className="card-link">
              See past semesters
            </a>
          </div>
        </div>
        <div className="card gedf-card">
          <div className="card-body">
            <h5 className="card-title">Live chat</h5>
            <a href="#" className="card-link">
              Enter
            </a>
          </div>
        </div>
      </div>
    </>
  );
}
