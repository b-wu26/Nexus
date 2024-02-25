import React from 'react'
import './Popup.css'

function InfoPopup(props) {
    return (props.trigger) ? (
        <div className="popup">
            <div className='popup-inner'>
                {/* <button className='submit-btn' onClick={() => props.setTrigger(false)}>
                    Submit
                </button> */}
                {props.children}
            </div>
        </div>
    ) : "";
}

export default InfoPopup