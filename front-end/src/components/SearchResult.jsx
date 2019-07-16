import React, { Component } from 'react';
import ItemList from "./ItemList";
import Pagination from "material-ui-flat-pagination";
import { withStyles } from '@material-ui/styles';
import Typography from '@material-ui/core/Typography';
import CircularProgress from '@material-ui/core/CircularProgress';

const style = {
  pagination: {
    margin: '20px auto'
  },
  total: {
    color: '#7D7D7D',
    margin: '10px'
  },
  progress: {
    display: 'flex',
    height: 200,
    justifyContent: 'center',
    alignItems: 'center'
  }
}

const pageSize = 10;
// const test = [
//   {
//     title: 'Spring 教程',
//     summary: 'Spring Boot makes it easy to create stand-alone, production-grade Spring based Applications that you can "just run". We take an opinionated view of the Spring ...',
//     date: '2015-12-25',
//     source: 'CSDN',
//     url: 'www.csdn.com',
//     tags: [ 'spring', 'java', 'backend']
//   },
//   {
//     title: 'Spring 教程',
//     summary: 'Spring Boot makes it easy to create stand-alone, production-grade Spring based Applications that you can "just run". We take an opinionated view of the Spring ...',
//     date: '2015-12-25',
//     source: 'CSDN',
//     url: 'www.csdn.com',
//     tags: [ 'spring', 'java', 'backend']
//   },
//   {
//     title: 'Spring 教程',
//     summary: 'Spring Boot makes it easy to create stand-alone, production-grade Spring based Applications that you can "just run". We take an opinionated view of the Spring ...',
//     date: '2015-12-25',
//     source: 'CSDN',
//     url: 'www.csdn.com',
//     tags: [ 'spring', 'java', 'backend']
//   }
// ]

const catalogs = ["全部资源", "介绍", "官方文档", "博客文章", "项目实战", "视频教程", "技术问答"];

class SearchResult extends Component {
  state = {
    query: this.props.query, //query={{"input": input, "catalog": catalog, "time": time }}
    page: 1,
    data: [],
    offset: 0,
    total: 0,
    loading: true
  }

  componentDidMount() {
    if(this.props.query)
      this.fetchData(this.props.query, 1);
  }

  // componentDidUpdate() {
  //   window.scrollTo(0, 0);
  //   this.fetchData(this.props.query, 1);
  // }

  componentWillReceiveProps(nextProps) {
    // console.log("query", nextProps.query);
    if(this.props.query !== nextProps.query) {
      this.setState({
        query: nextProps.query,
        page: 1,
        offset: 0,
        loading: true
      })
      this.fetchData(nextProps.query, 1);
    }
    
  }
  
  fetchData = (query, page=1) => {
    const input = query.input;
    const catalog = query.catalog || -1;
    const time = query.time || 0;
    const url = `http://10.214.213.43:9999/search?key=${input}&catalog=${catalog}&page=${page}&size=${pageSize}&delta=${time}`;
    
    if(input) {
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
    }
    setTimeout(() => {
      window.scrollTo(0, 0);
    }, 1000);
  }

  changePage = (offset) => {
    const page = 1 + offset / pageSize;
    this.setState({ 
      offset: offset,
      page: page,
      loading: true
    });
    this.fetchData(this.state.query, page);
  }

  render() {
    const {classes, query} = this.props;
    const { offset, data, total, loading } = this.state;
    return (
      loading ? 
      ( <div className={classes.progress}>
          <CircularProgress />
        </div>) : (
        <div>
        <Typography variant="subtitle1" component="h2" className={classes.total}>
          [ {catalogs[query.catalog + 1]} ] - 显示 {total} 条最优搜索结果
        </Typography>
        <ItemList data={data}/>
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

export default withStyles(style)(SearchResult);
