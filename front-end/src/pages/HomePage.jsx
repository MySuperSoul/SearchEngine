import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import IconButton from '@material-ui/core/IconButton';
import { FindInPage, Favorite } from '@material-ui/icons';
import backgroundImg from '../assets/images/background.jpg';
import SearchBar from '../components/SearchBar';
import logo from '../assets/images/logo-white.png';


const style = theme => ({
  root: {
    height: '100%'
  },
  wrapper: {
    width: '100%',
    height: '100%',
    // display: 'flex',
    // flexDirection: 'column',
    // justifyContent: 'center',
    // alignItems: 'center',
    background: `url(${backgroundImg}) no-repeat center`,
    backgroundSize: 'cover',
    position: 'fixed'
  },
  title: {
    margin: '15px',
    color: '#ffffff'
  },
  // iconButton: {
  //   padding: 10,
  // },
  // searchBar: {
    
  // },
  // input: {
  //   paddingLeft: '15px'
  // },
  navLinks: {
    marginLeft: 'auto',
    marginRight: '0'
  },
  linkItem: {
    margin: '0 10px'
  },
  navBar: {
    backgroundColor: 'transparent',
    color: "#ffffff",
    boxShadow: '0 0 0 0',
    padding: '20px 30px'
  },
  content: {
    height: '90%',
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
  },
  footer: {
    textAlign: 'center',
    color: '#ffffff',
    marginTop: '20px'
  },
  loveIcon: {
    fontSize: '1rem',
    padding: '2px 5px'
  }
});

class HomePage extends React.Component {
  state = {
    input: "",
  }

  render() {
    const { classes } = this.props;
    return (
      <div className={classes.root}>
        <div className={classes.wrapper}>
          <AppBar position="absolute" className={classes.navBar}>
            <Toolbar>
              <IconButton edge="start" className={classes.menuButton} color="inherit" aria-label="Menu">
                <FindInPage />
              </IconButton>
              <Typography variant="subtitle1" >
                技术知识，一搜便知
              </Typography>
              {/* <div className={classes.navLinks}>
                <Button color="inherit" className={classes.linkItem}> 
                  使用手册 
                </Button>
                <Button color="inherit" className={classes.linkItem}> 
                  项目实战 
                </Button>
                <Button color="inherit" className={classes.linkItem}> 
                  技术问答 
                </Button>
              </div> */}
            </Toolbar>
          </AppBar>
          <div className={classes.content}>
            <div className={classes.title}>
              <img src={logo} alt="techhub logo" style={{width: 350}}/>
            </div>
            <SearchBar />
          </div>
          <footer className={classes.footer}> 
            <Typography variant="body2" component="p">
              made with 
              <Favorite className={classes.loveIcon}/>
              by Group-8 @ZJU
            </Typography>
          </footer>
        </div>
      </div>
    );
  }
}

export default withStyles(style)(HomePage);