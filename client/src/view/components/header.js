import React, { Component } from 'react'
import { Link } from "react-router-dom";
import 'jqueryui'
import Cookies from "universal-cookie";

class Header extends Component {

    componentDidMount() {
    }

    numberWithCommas(x) {
        return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }

    render() {


        return (
            <div className="header-wrapper">

                <div className="header">

                    <div className="header-left">
                        <ul>
                            <li>
                                <Link to="/" className="button-border">
                                  Video Conversion
                                </Link>
                            </li>
                        </ul>
                    </div>

                    <div className="header-center">
                        <Link to="/">
                            Video Conversion Client
                        </Link>
                    </div>

                    <div className="header-right">
                    </div>

                </div>

            </div>
        )

    }

}

export default Header
