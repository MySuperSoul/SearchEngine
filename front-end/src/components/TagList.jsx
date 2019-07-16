import React, { Component } from 'react'
import withStyles from "@material-ui/core/styles/withStyles";
import Chip from '@material-ui/core/Chip';
import { LabelOutlined } from '@material-ui/icons';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import { Link } from 'react-router-dom';
import Pagination from "material-ui-flat-pagination";
import CircularProgress from '@material-ui/core/CircularProgress';

const style = {
  container: {
    display: 'flex',
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'flex-start'
  },
  tag: {
    margin: '10px 5px',
  },
  title: {
    margin: 10
  },
  grid: {
    margin: '5px 0'
  },
  pagination: {
    margin: '20px auto'
  },
  progress: {
    display: 'flex',
    height: 200,
    justifyContent: 'center',
    alignItems: 'center'
  }
}

// const data = [
//   {tag: "Spring Cloud", count: 20},
//   {tag: "Spring Boot", count: 40},
//   {tag: "Docker", count: 100},
//   {tag: "Eureka", count: 10},
//   {tag: "Turbine", count: 20},
//   {tag: "Zuul", count: 20},
//   {tag: "Archaius", count: 20},
//   {tag: "Consul", count: 20},
//   {tag: "Spring Cloud Bus", count: 20},
//   {tag: "Ribbon", count: 20},
// ];

const pageSize = 24;
class TagList extends Component {
  state = {
    data: [],
    total: 0,
    page: 1,
    offset: 0,
    loading: true,
  };

  componentDidMount() {
    this.fetchData(1);
  }

  fetchData = (page=1) => {
    const url = `http://10.214.213.43:9999/getAllTag?page=${page}&size=${pageSize}&key=`;
    fetch(url)
      .then(res => res.json())
      .then((json) => {
        if(json.code === 200) {
          this.setState({
            data: json.data.result,
            total: json.data.total,
            loading: false
          })
        }
      })
    
    // setTimeout(() => {
      window.scrollTo(0, 0);
    // }, 1000);
  }

  changePage = (offset) => {
    const page = 1 + offset / pageSize;
    this.setState({ 
      offset: offset,
      page: page,
      // loading: true
    });
    this.fetchData(page);
  }

  render() {
    const { classes } = this.props;
    const {data, total, offset, loading} = this.state;
    return (
      loading ? (<div className={classes.progress}>
        <CircularProgress />
      </div>) : (
      <div>
        <Typography variant="subtitle1" component="h2" className={classes.title}>
          共计 {total} 个技术标签：
        </Typography>
        <Grid container className={classes.root}>
            { data.map((item, index) => (
              <Grid item xs={3} className={classes.grid} key={index}>
                <Link to={`/search/tags/${item.tag}`} style={{textDecoration: 'none'}}>
                  <Chip
                    icon={<LabelOutlined style={{fontSize: '18px'}}/>}
                    label={item.tag}
                    color="primary"
                    className={classes.tag}
                    variant="outlined"
                    // component="a"
                    // href={`/search/tags/${item.tag}`}
                    clickable
                  />
                </Link>
                <Typography variant="caption" component="span">
                  × {item.count}
                </Typography>
                {/* <span> {item.count} </span> */}
               </Grid>
            ))}
        </Grid>
        <div className={classes.pagination}>
          <Pagination
            limit={pageSize}
            offset={offset}
            total={total}
            onClick={(event, offset) => this.changePage(offset)}
            otherPageColor="default"
            currentPageColor="secondary"
          />
        </div>
      </div>

      )

    )
  }
}

export default withStyles(style)(TagList);