import React, { useState, useEffect } from "react";
import InputField from "../../../utils/InputField";
import LeftSidebar from "../LeftSidebar";
import CourseListItem from "./CourseListItem";
import Navbar from "../Navbar";
import axios from "axios";
import { BACKEND_SERVER_DOMAIN } from "../../../settings";

export default function CourseSearch() {
  const [course_name, setCourseName] = useState("");
  const [course_level, setCourseLevel] = useState("1");
  const [faculty, setFaculty] = useState("ECE");
  const [submitted, setSubmitted] = useState(false);
  const [courses, setCourses] = useState([]);

  function handleCourseNameChange(e) {
    setCourseName(e.target.value);
  }

  function handleCourseLevelChange(e) {
    setCourseLevel(e.target.value);
  }

  function handleFacultyChange(e) {
    setFaculty(e.target.value);
  }

  function onSubmit() {
    const data = new FormData();
    data.append("course_name", course_name);
    data.append("course_level", course_level);
    data.append("faculty", faculty);

    const config = {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    };

    axios
      .post(`${BACKEND_SERVER_DOMAIN}/api/search_courses`, data, config)
      .then(function (response) {
        setCourses(response.data);
        setSubmitted(true);
      })
      .catch(function (error) {
        console.log(error.response.data);
      });
  }

  function resetPage() {
    setSubmitted(false);
    setCourses([]);
  }

  return (
    <section className="course-search">
      <Navbar />
      <div className="navbar-spacer"></div>
      <div className="container">
        <div className="row">
          <div className="col-lg-3 col-12">
            <LeftSidebar active={3} />
          </div>
          <div className="col-lg-6 col-12 timeline">
            <div className="d-flex justify-content-between align-items-center">
              <h3 style={{ marginTop: "20px", marginBottom: "20px" }}>
                Search Courses
              </h3>
              {submitted && (
                <button
                  type="submit"
                  onClick={resetPage}
                  className="btn btn-primary btn-signup">
                  Search Again
                </button>
              )}
            </div>
            {!submitted ? (
              <div className="col g-3">
                <div className="d-flex flex-column">
                  <label className="form-label">Faculty</label>
                  <select onChange={handleFacultyChange}>
                    <option value="ECE">ECE</option>
                    <option value="CS">CS</option>
                    <option value="SYDE">SYDE</option>
                  </select>
                </div>
                <div className="d-flex flex-column mt-3">
                  <label className="form-label">Course Level</label>
                  <select onChange={handleCourseLevelChange}>
                    <option value="1">1xx</option>
                    <option value="2">2xx</option>
                    <option value="3">3xx</option>
                    <option value="4">4xx</option>
                    <option value="5">5xx</option>
                    <option value="6">6xx</option>
                    <option value="7">7xx</option>
                  </select>
                </div>
                <div className="d-flex flex-column mt-3">
                  <InputField
                    label="Course Name"
                    type="text"
                    name={"course_name"}
                    placeholder="Optional"
                    onChange={handleCourseNameChange}
                    value={course_name}
                  />
                </div>
                <div className="col-12 mt-4">
                  <button
                    type="submit"
                    onClick={onSubmit}
                    className="btn btn-primary btn-signup"
                  >
                    Search
                  </button>
                </div>
              </div>
            ) : (
              <div>
                {courses.map(
                  (course) => (
                    <div key={course.idclass_profile}>
                      <div className="card">
                        <CourseListItem
                          key={course.idclass_profile}
                          course={{
                            "course_code": course.faculty + course.course_code,
                            "class_name": course.class_name,
                            "idclass_profile": course.idclass_profile
                          }}
                        />
                      </div>
                    </div>
                  )
                )}

              </div>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}
