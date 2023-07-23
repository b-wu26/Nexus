import React from "react";
import Feed from "./Feed";

export default function Content() {
  return (
    <>
      <div className="col-md-6 gedf-main">
        <div className="card gedf-card">
          <div className="card-header">
            <ul
              className="nav nav-tabs card-header-tabs"
              id="myTab"
              role="tablist"
            >
              <li className="nav-item">
                <a
                  className="nav-link active"
                  id="posts-tab"
                  data-toggle="tab"
                  href="#posts"
                  role="tab"
                  aria-controls="posts"
                  aria-selected="true"
                >
                  Create post
                </a>
              </li>
              <li className="nav-item">
                <a
                  className="nav-link"
                  id="images-tab"
                  data-toggle="tab"
                  role="tab"
                  aria-controls="images"
                  aria-selected="false"
                  href="#images"
                >
                  Files
                </a>
              </li>
            </ul>
          </div>
          <div className="card-body">
            <div className="tab-content" id="myTabContent">
              <div
                className="tab-pane fade show active"
                id="posts"
                role="tabpanel"
                aria-labelledby="posts-tab"
              >
                <div className="form-group">
                  <label className="sr-only" for="message">
                    post
                  </label>
                  <textarea
                    className="form-control"
                    id="message"
                    rows="3"
                    placeholder="Text"
                  ></textarea>
                </div>
              </div>
              <div
                className="tab-pane fade"
                id="images"
                role="tabpanel"
                aria-labelledby="images-tab"
              >
                <div className="form-group">
                  <div className="custom-file">
                    <input
                      type="file"
                      className="custom-file-input"
                      id="customFile"
                    />
                    <label className="custom-file-label" for="customFile">
                      Upload file
                    </label>
                  </div>
                </div>
                <div className="py-4"></div>
              </div>
            </div>
            <div className="btn-toolbar justify-content-between">
              <div className="btn-group">
                <button type="submit" className="btn btn-primary">
                  Post
                </button>
              </div>
            </div>
          </div>
        </div>
        <Feed />
      </div>
    </>
  );
}
