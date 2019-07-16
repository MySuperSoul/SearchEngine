import React, { Component } from 'react'
import { withStyles } from '@material-ui/core/styles';
import { Favorite, CloudCircle } from '@material-ui/icons';
import Typography from '@material-ui/core/Typography';
import NavBar from '../components/NavBar';
import Grid from '@material-ui/core/Grid';
import Filter from "../components/Filter";
import SideBar from "../components/SideBar";
import SearchResult from "../components/SearchResult";
import { Switch, Route } from 'react-router-dom';
import TagList from '../components/TagList';
import TagResult from '../components/TagResult';
import TagCloud from '../components/TagCloud';
import ScrollTop from '../components/ScrollTop';

const style = theme => ({
  main: {
    backgroundColor: '#F9F7F7',
    minHeight: 750
  },
  wrapper: {
    padding: '100px 35px 15px 35px',
    [theme.breakpoints.down("xs")]: {
      padding: "10px 10px"
    }
  },
  navBar: {
    backgroundColor: 'transparent',
    boxShadow: '0 0 0 0',
    padding: '20px'
  },
  content: {
    padding: '0 20px',
    minHeight: 560
  },
  sider: {

  },
  // filter: {
  //   height: '50px',
  //   width: '50%'
  // },
  pagination: {
    margin: '20px auto'
  },
  footer: {
    textAlign: 'center',
    color: '7D7D7D',
    marginTop: '80px',
  },
  loveIcon: {
    fontSize: '1rem',
    padding: '2px 5px'
  }
});

class ResultPage extends Component {
  state = {
    input: this.props.match.params.input,
    loading: true,
    catalog: -1,
    time: 0
  }

  componentDidMount() {
    // console.log(this.props);
  }

  componentWillReceiveProps(nextProps) {
    if(nextProps.match.params.input &&
    (this.props.match.params.input !== nextProps.match.params.input)) {
      this.setState({
        input: nextProps.match.params.input
      })
    }
  }

  changeCatalog = (catalog) => {
    this.setState({catalog});
    // console.log("catalog", catalog);
  }

  changeTime = (time) => {
    this.setState({time});
    // console.log("time", time);
  }

  render() {
    const {classes} = this.props;
    const { input, catalog, time } = this.state;

    return (
      <div className={classes.main}>
        <NavBar className={classes.NavBar} />
        <div className={classes.wrapper}>
          <Grid container spacing={4} className={classes.content}>
            <Grid item xs={12} sm={3} md={2} className={classes.sider}>
              <SideBar input={input} changeCatalog={this.changeCatalog} />
            </Grid>
            <Grid item xs={12} sm={6} md={7}>
              <Switch>
                <Route path="/search/query/:input" 
                  render={() => <SearchResult query={{"input": input, "catalog": catalog, "time": time }}/>}
                />
                <Route path="/search/tags/all" component={TagList} />
                <Route path="/search/tags/:tag" component={TagResult} />
              </Switch>
            </Grid>
            <Grid item xs={12} sm={3} md={3} className={classes.sider}>
              { this.props.location.pathname.indexOf("tags") < 0 && 
                <Filter changeTime={this.changeTime} /> 
              }
              <Typography variant="subtitle1" component="h2" style={{color: '#7D7D7D', margin:'25px 0'}}>
                <CloudCircle /> 标签词云
              </Typography>
              <TagCloud />
            </Grid>
          </Grid>
          <ScrollTop />
          <footer className={classes.footer}>
            <Typography variant="body1" component="p" style={{color: '#7D7D7D'}}>
              made with 
              <Favorite className={classes.loveIcon}/>
              by Group-8 @ZJU
            </Typography>
          </footer>
        </div>
      </div>
    )
  }
}

export default withStyles(style)(ResultPage);