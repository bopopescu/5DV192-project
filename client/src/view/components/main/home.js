import React, { Component } from 'react'
import { Wrapper } from "../../containers/wrapper";
import $ from 'jquery';


class Home extends Component {

    constructor(props) {

        super(props);

        this.handleClick = this.handleClick.bind(this);

    }

    handleClick() {

        let filename = $('input[type=file]').val().split('\\').pop();
        $('#file-name').html(filename);

    }

    render() {
        return (
            <Wrapper>
                <div className="content-inner">
                    <div className="file-input">
                        <input type="file" id="file-upload" onChange={() => this.handleClick()} />
                        <span className="label" id="file-name">No file selected</span>
                        <span className="button">Choose</span>
                    </div>
                </div>
            </Wrapper>
        )
    }

}

export default Home
