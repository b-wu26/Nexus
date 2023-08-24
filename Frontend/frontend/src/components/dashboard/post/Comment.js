import React, { useState, useRef, useEffect } from "react";

export default function CommentComponent() {

    function splicedArray(array, index) {
        let nArr = [...array];
        nArr.splice(0, index + 1);
        return nArr;
    }

    return (
        <div className="d-flex comment">
            
        </div>
    );
}
