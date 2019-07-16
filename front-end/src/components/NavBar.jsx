import React, { Component } from 'react'
import { withStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import SearchBar from './SearchBar';
import logo from '../assets/images/logo-white.png';
import github from '../assets/images/GitHubIcon.png';
import { Link } from 'react-router-dom';
import IconButton from '@material-ui/core/IconButton';
import Tooltip from '@material-ui/core/Tooltip';

const style = theme => ({
  navBar: {
    backgroundColor: '#724de4',
    // boxShadow: '0 0 0 0',
    color: '#2D2D2D',
    // paddingTop: '20px'
  },
  toolBar: {
    padding: '0 25px',
    [theme.breakpoints.down("xs")]: {
      padding: "0 2vw"
    }
  },
  navLinks: {
    marginLeft: 'auto',
    marginRight: '30px'
  },
  linkItem: {
    margin: '0 10px'
  },
  searchBar: {
    padding: '0 50px'
  },
  logo: {
    width: '13rem',
    margin: '5px 45px 5px 15px'
  },
  github: {
    width: '35px'
  }
});

class NavBar extends Component {
  render() {
    const { classes } = this.props;
    return (
      <AppBar position="fixed" className={classes.navBar}>
        <Toolbar className={classes.toolBar}>
          <Link to='/'>
            <img src={logo} alt="techhub logo" className={classes.logo}/>
          </Link>
          {/* <Typography variant="h5" style={{ marginRight: '20px'}}>
            TechHub
          </Typography> */}
          <SearchBar />
          <div className={classes.navLinks}>
            <Tooltip title="GitHub" aria-label="GitHub">
              <IconButton aria-label="Github" href='https://github.com/MySuperSoul/SearchEngine' target='_blank'>
                <img src={github} alt="github link" className={classes.github} />
              </IconButton>
            </Tooltip>
            
            {/* <Button color="inherit" className={classes.linkItem}>
              使用手册 
            </Button>
            <Button color="inherit" className={classes.linkItem}> 
              项目实战 
            </Button>
            <Button color="inherit" className={classes.linkItem}> 
              技术问答 
            </Button> */}
          </div>
        </Toolbar>
      </AppBar>
    )
  }
}

export default withStyles(style)(NavBar);