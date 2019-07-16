import React from "react";
import WordCloud from "react-d3-cloud";
import '../assets/css/wordcloud.css';

const wordcloudcss={
		// backgroundImage: "linear-gradient(to left, #fbc2eb 0%, #a6c1ee 100%)",
		backgroundColor: '#ffffff',
    width: "300px",
    margin: "30px 0 10px 0",
    minHeight: "300px",
    boxSizing: "border-box",
		borderRadius: "10px",
		boxShadow: "0px 1px 3px 0px rgba(0,0,0,0.2)"
		// border: 'solid 1px #dddddd'
}

// const data = [
// 	{ text: "Hey", value: 1000 },
// 	{ text: "duck", value: 10 },
// 	{ text: "lol", value: 200 },
// 	{ text: "first impression", value: 800 },
// 	{ text: "黄亦非", value: 10000 },
// 	{ text: "duck", value: 10 },
// 	{ text: "lol", value: 200 },
// 	{ text: "first impression", value: 800 },
// 	{ text: "陈鑫", value: 10000 },
// 	{ text: "duck", value: 10 },
// 	{ text: "lol", value: 200 },
// 	{ text: "first impression", value: 800 },
// 	{ text: "傅诤哲", value: 10000 },
// 	{ text: "duck", value: 10 },
// 	{ text: "lol", value: 200 },
// 	{ text: "first impression", value: 800 },
// 	{ text: "胡瀚丹", value: 10000 },
// 	{ text: "duck", value: 10 },
// 	{ text: "lol", value: 200 },
// 	{ text: "first impression", value: 800 },
// ];

export default class TagCloud extends React.Component  {
	state = {
		data: []
	}

	componentDidMount() {
		const url = `http://10.214.213.43:9999/getAllTag?page=1&size=50&key=`;
		fetch(url)
		.then(res => res.json())
		.then((json) => {
			if(json.code === 200) {
				let tags = json.data.result;
				let data = tags.map(o => {
					return {
						text: o.tag, value: o.count
					}
				});
				this.setState({
					data: data
				})
			}
		})
	}

	render() {
		const {data} = this.state;
		const fontSizeMapper = word => Math.log2(word.value)*2;
		const rotate = word => Math.floor(word.value % 360/290)*45;
		// const tagdetail= word =>{window.location.href="https://www.baidu.com/s?wd="+word.text};
		const tagdetail= word => {window.location.href=`/search/tags/${word.text}`}

		const height=this.props.height || 300;
		const width=this.props.width || 300;
		return(
			<div style={wordcloudcss}>
				<WordCloud data={data} height={height} width={width} font={"'Noto Sans SC', sans-serif"} fontSizeMapper={fontSizeMapper} rotate={rotate} onWordClick={tagdetail}/>
			</div>
		)
	}
}

