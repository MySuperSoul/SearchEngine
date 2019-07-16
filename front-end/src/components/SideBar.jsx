import React, { Component } from 'react';
import withStyles from "@material-ui/core/styles/withStyles";
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import Collapse from '@material-ui/core/Collapse';
import { ChromeReaderMode, Explore, LabelImportant, FormatListBulleted, Code, Description, OndemandVideo, QuestionAnswer} from '@material-ui/icons';
import ExpandLess from '@material-ui/icons/ExpandLess';
import ExpandMore from '@material-ui/icons/ExpandMore';
import { Link, withRouter } from 'react-router-dom';

const style = {
  root: {
    width: '100%',
    maxWidth: 360,
  },
  nested: {
    paddingLeft: 40,
  },
};

const catalogs = ["官方文档", "博客文章", "项目实战", "视频教程", "技术问答"];
const mapIcons = [
  <Description />,
  <ChromeReaderMode />,
  <Code />,
  <OndemandVideo />,
  <QuestionAnswer />,
];

class SideBar extends Component {
  state = {
    input: this.props.input,
    open: true,
    selectedIndex: -1,
    catalog: -1
  }

  componentDidMount() {
    // console.log(this.props);
    if(this.props.location.pathname.indexOf("tags") > 0) 
      this.setState({
        selectedIndex: -2
      })
  }

  handleClick = () => {
    this.setState(prevState => ({
        open: !prevState.open
    }))
  }

  componentWillReceiveProps(nextProps) {
    if(nextProps.input !== this.props.input) {
      this.setState({
        selectedIndex: -1
      })
    }
  }

  handleSelect = (event, index) =>{
    this.setState({
      selectedIndex: index
    })
  }

  selectCatalog = (event, index) =>{
    this.setState({
      selectedIndex: index
    })
    this.props.changeCatalog(index);
  }
  
  render() {
    const {classes, input} = this.props;
    const { open, selectedIndex} = this.state;
    const inputUrl = input ? `/search/query/${input}` : this.props.location.pathname;
    return (
      <List
        component="nav"
        aria-labelledby="资源分类菜单"
        // subheader={
        //   <ListSubheader component="div" id="nested-list-subheader">
        //     分类
        //   </ListSubheader>
        // }
        className={classes.root}
      >
        <Link to={inputUrl} style={{textDecoration: "none", color: "inherit"}}>
          <ListItem button selected={selectedIndex === -1} onClick={event => this.selectCatalog(event, -1)}>
          <ListItemIcon>
            <Explore />
          </ListItemIcon>
          <ListItemText primary="所有资源" />
        </ListItem>
        </Link>
        <ListItem button onClick={this.handleClick}>
          <ListItemIcon color="primary">
            <FormatListBulleted />
          </ListItemIcon>
          <ListItemText primary="分类" />
          {open ? <ExpandLess /> : <ExpandMore />}
        </ListItem>
        <Collapse in={open} timeout="auto" unmountOnExit>
          <List component="div" disablePadding>
            {
              catalogs.map((item, index) => (
                <Link key={index} to={`/search/query/${input}`} style={{textDecoration: "none", color: "inherit"}}>
                  <ListItem button className={classes.nested}
                    selected={selectedIndex === (catalogs.indexOf(item)+1)}
                    onClick={event => this.selectCatalog(event, (catalogs.indexOf(item)+1))}>
                    <ListItemIcon>
                      {mapIcons[index]}
                    </ListItemIcon>
                    <ListItemText primary={item} />
                  </ListItem>
                </Link>
              ))
            }
          </List>
        </Collapse>
        <Link to="/search/tags/all" style={{textDecoration: "none", color: "inherit"}}>
          <ListItem button selected={selectedIndex === -2} onClick={event => this.handleSelect(event, -2)}>
            <ListItemIcon>
              <LabelImportant />
            </ListItemIcon>
            <ListItemText primary="标签" />
          </ListItem>
        </Link>
      </List>
    );
  }
}

const styledBar = withStyles(style)(SideBar)
export default withRouter(styledBar);