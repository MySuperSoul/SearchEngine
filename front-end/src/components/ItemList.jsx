import React, { Component } from 'react'
import ItemCard from './ItemCard';
import withStyles from "@material-ui/core/styles/withStyles";

const style = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center'
  }
}

class ItemList extends Component {
  render() {
    const { classes, data } = this.props;
    return (
      <div className={classes.container}>
        { data.map((item, index) => (
          <ItemCard key={index} data={item} />
        ))}
      </div>
    )
  }
}

export default withStyles(style)(ItemList);