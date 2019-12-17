import React, { Component } from 'react'
import { Wrapper } from "../containers/wrapper";
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

        this.handleFileChange = this.handleFileChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);

        this.props.actionTranscoderReset();

        this.state = {
            isSubmitted: false,
            input: {
                filename: "",
            },
            output: {
                filename: "output",
                resolution: "Unchanged",
                compression: "Unchanged",
                format: "MP4",
            }
        }


    }

    handleFileChange(e, key) {
        let filename = $('input[type=file]').val().split('\\').pop();
        $('#file-name').html(filename);
        let newState = JSON.parse(JSON.stringify(this.state));
        newState.input[key] = filename;
        this.setState(newState);
    }

    handleChangeOutput(e, key) {
        let newState = JSON.parse(JSON.stringify(this.state));
        newState.output[key] = e.target.value;
        this.setState(newState);
    }

    handleSubmit(e) {

        e.preventDefault();


        if (document.getElementById('file-upload').files[0]) {

            let newState = JSON.parse(JSON.stringify(this.state));
            newState.isSubmitted = true;
            this.setState(newState);

            let file = document.getElementById('file-upload').files[0];

            let reader = new FileReader();
            reader.onload = this.handleFileLoad;
            reader.readAsText(file);

            const data = new FormData();
            data.append('file', file);

            let keys = Object.keys(this.state.input);
            for(let k of keys){
                data.append("input-" + k, this.state.input[k]);
            }

            keys = Object.keys(this.state.output);
            for(let k of keys){
                data.append("output-" + k, this.state.output[k]);
            }

            this.props.actionTranscoderSend(data);

            console.log(this.props.transcoder);

        }



    }

    handleFileLoad(event) {
        console.log(event.target.result);
    }

    render() {

        let html = [];

        html.resolutions = resolutions.map((item) =>
            <option value={item} key={item}>{item}</option>
        );
        html.compressions = compressions.map((item) =>
            <option value={item} key={item}>{item}</option>
        );
        html.formats = formats.map((item) =>
            <option value={item} key={item}>{item}</option>
        );

        let response = [];

        if(this.props.transcoder && this.props.transcoder.isFetched) {
            if(this.props.transcoder.success) {
                response.push(
                    <div className="alert alert-green">
                        <p>Success!</p>
                    </div>
                )
            } else {
                response.push(
                    <div className="alert alert-red">
                        <p>Failure</p>
                    </div>
                )
            }
        } else {
            response.push(
                <div className="lds-spinner-container">
                    <div className="lds-spinner">
                        <div></div>
                        <div></div>
                        <div></div>
                        <div></div>
                        <div></div>
                        <div></div>
                        <div></div>
                        <div></div>
                        <div></div>
                        <div></div>
                        <div></div>
                        <div></div>
                    </div>
                </div>
            )
        }


        return (
            <Wrapper>
                <div className="content-inner">
                    <form className="transcoder" onSubmit={this.handleSubmit}>
                        <h1>Input</h1>
                        <div className="file-input-container">
                            <h2>File</h2>
                            <div className="file-input">
                                <input type="file" id="file-upload" onChange={(e) => this.handleFileChange(e, "filename")} />
                                <span className="label" id="file-name">No file selected</span>
                                <button type="button" className="button button-blue">Choose</button>
                            </div>
                        </div>
                        <h1>Output</h1>
                        <div className="file-setting-container">
                            <h2>Resolution</h2>
                            <div className="file-setting">
                                <select name="resolution" id="resolution" value={this.state.output.resolution} onChange={(e) => this.handleChangeOutput(e, "resolution")}>
                                    {html.resolutions}
                                </select>
                            </div>
                        </div>
                        <div className="file-setting-container">
                            <h2>Quality</h2>
                            <div className="file-setting">
                                <select name="compression" id="compression" value={this.state.output.compression} onChange={(e) => this.handleChangeOutput(e, "compression")}>
                                    {html.compressions}
                                </select>
                            </div>
                        </div>
                        <div className="file-setting-container">
                            <h2>Format</h2>
                            <div className="file-setting">
                                <select name="format" id="format" value={this.state.output.format} onChange={(e) => this.handleChangeOutput(e, "format")}>
                                    {html.formats}
                                </select>
                            </div>
                        </div>
                        <div className="file-setting-container">
                            <h2>Filename</h2>
                            <div className="file-setting">
                                <input type="text" name="filename" id="filename" value={this.state.output.filename} onChange={(e) => this.handleChangeOutput(e, "filename")} />
                            </div>
                        </div>
                        <div className="file-save">
                            <button type="submit" className="button button-blue">Transcode</button>
                        </div>
                        {this.state.isSubmitted && (
                            response
                        )}
                    </form>
                </div>
            </Wrapper>
        )
    }

}

export default Home