import React, { Component } from 'react'
import { ArrowUpward } from '@material-ui/icons';
import Fab from '@material-ui/core/Fab';

export default class ScrollTop extends Component {
  state = {
    show: false
  }

  componentDidMount(){
    window.addEventListener('scroll' , ()=>{
      let scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
      if(scrollTop > 500){
        this.setState({
          show : true
        })
      }else{
        this.setState({
          show : false
        })
      }
    })
  }

  goTo = () => {
    let scrollToTop = window.setInterval(function() {
      let pos = window.pageYOffset;
      if ( pos > 0 ) {
          window.scrollTo( 0, pos - 20 ); // how far to scroll on each step
      } else {
          window.clearInterval( scrollToTop );
      }
  }, 2);
  }

  render() {
    let { show } = this.state;
    return (
      <div className="common-back">
        {
          show &&
          <Fab color="secondary" aria-label="Add" onClick={this.goTo} 
            style={{position:'fixed', display: 'block', bottom: '100px', right:'100px'}}
          >
            <ArrowUpward />
          </Fab>
        }
          
      </div>
    );
  }
}
