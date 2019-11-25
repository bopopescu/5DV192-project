import React, { Component } from 'react'
import { Wrapper } from "../../containers/wrapper";


class Home extends Component {

    render() {
        return (
            <Wrapper>
                <div className="content-inner">
                    <input type="file" name="file" id="file" onChange=""/>
                </div>
            </Wrapper>
        )
    }

}

export default Home
