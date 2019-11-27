import React, { Component } from 'react'
import { Wrapper } from "../../containers/wrapper";
import $ from 'jquery';


const resolutions = [
    "Unchanged", "240p", "480p", "720p", "1080p", "2K", "4K"
];
const compressions = [
    "Unchanged", "Low", "Medium", "High"
];
const formats =  [
    "MP4", "AVI", "MKV"
];

class Home extends Component {

    constructor(props) {

        super(props);

        this.handleClick = this.handleClick.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);

        this.state = {
            resolution: "Unchanged",
            compression: "Unchanged",
            format: "MP4",
            filename: "output",
        }


    }

    handleClick() {
        let filename = $('input[type=file]').val().split('\\').pop();
        $('#file-name').html(filename);
    }

    handleChange(e, key) {
        let newState = JSON.parse(JSON.stringify(this.state));
        newState[key] = e.target.value;
        this.setState(newState);
    }

    handleSubmit(e) {
        e.preventDefault();
        console.log(this.state)
    }

    render() {

        let html = [];

        html.resolutions = resolutions.map((item, key) =>
            <option value={item} key={item}>{item}</option>
        );

        html.compressions = compressions.map((item, key) =>
            <option value={item} key={item}>{item}</option>
        );

        html.formats = formats.map((item, key) =>
            <option value={item} key={item}>{item}</option>
        );



        return (
            <Wrapper>
                <div className="content-inner">
                    <form className="transcoder" onSubmit={this.handleSubmit}>
                        <h1>Input</h1>
                        <div className="file-input-container">
                            <h2>File</h2>
                            <div className="file-input">
                                <input type="file" id="file-upload" onChange={() => this.handleClick()} />
                                <span className="label" id="file-name">No file selected</span>
                                <button className="button button-blue">Choose</button>
                            </div>
                        </div>
                        <h1>Output</h1>
                        <div className="file-setting-container">
                            <h2>Resolution</h2>
                            <div className="file-setting">
                                <select name="resolution" id="resolution" value={this.state.resolution} onChange={(e) => this.handleChange(e, "resolution")}>
                                    {html.resolutions}
                                </select>
                            </div>
                        </div>
                        <div className="file-setting-container">
                            <h2>Quality</h2>
                            <div className="file-setting">
                                <select name="compression" id="compression" value={this.state.compression} onChange={(e) => this.handleChange(e, "compression")}>
                                    {html.compressions}
                                </select>
                            </div>
                        </div>
                        <div className="file-setting-container">
                            <h2>Format</h2>
                            <div className="file-setting">
                                <select name="format" id="format" value={this.state.format} onChange={(e) => this.handleChange(e, "format")}>
                                    {html.formats}
                                </select>
                            </div>
                        </div>
                        <div className="file-setting-container">
                            <h2>Filename</h2>
                            <div className="file-setting">
                                <input type="text" name="filename" id="filename" value={this.state.filename} onChange={(e) => this.handleChange(e, "filename")} />
                            </div>
                        </div>
                        <div className="file-save">
                            <button type="submit" className="button button-blue">Transcode</button>
                        </div>
                    </form>
                </div>
            </Wrapper>
        )
    }

}

export default Home