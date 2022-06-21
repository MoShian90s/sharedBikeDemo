<template>
<el-card  class='box-card' shadow='always' body-style="display:flex;justify-content:center;align-items:center;padding:5% 7% 5% 7%">
	<el-form size="medium" style="width:100%">
		<el-form-item>
			<el-select v-model="SelectField" placeholder="field" style="width:100%">
				<el-option label="🆔 Unique ID" value="Customer_id"></el-option>
				<el-option label="🔠 First Name" value="Customer_first_name"></el-option>
				<el-option label="🔠 Last Name" value="Customer_last_name"></el-option>
				<el-option label="👶 Age" value="Customer_age"></el-option>
				<el-option label="👫 Gender" value="Customer_gender"></el-option>
				<el-option label="📞 Phone" value="Customer_phone_num"></el-option>
			</el-select>
		</el-form-item>
		<el-form-item>
			<el-input placeholder="Search Key Word" v-model="keyword"></el-input>
		</el-form-item>
		<el-form-item>
			<el-button icon="el-icon-search" round class="SearchBtn" @click.native="Search">Search</el-button>
		</el-form-item>
	</el-form>
</el-card>
</template>

<script>
import axios from 'axios';
import qs from 'qs';
import {sharedStore} from '../Table'

export default {
    data(){
        return{
            keyword:'',
			SelectField:'Customer_id',
        }
    },
    methods:{
        Search(){
            let that=this;
            let payload=qs.stringify({type:that.SelectField,keyword:that.keyword});
            axios.post(that.$baseURL+"/manager/searchcustomerinfo/",payload)
                .then(function(response) {
                    let data=[];
                    response.data.forEach(element => {
                        data.push(element['fields'])
                    });
                    sharedStore.tableData=data;
                    that.$notify.success({
                        title:'Search Operation',
                        message:'system is returning ' + that.keyword
                    });
                })
                .catch(function () {
                    that.$notify.error({
                        title:'Search Operation',
                        message:'no results found'
                    });
            });
        }
    }
}
</script>

<style scoped>
.SearchBtn{
    width:100%;
    margin-top:3vh;
}
.SearchBtn:hover{
    box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04)
}
.scale-in-center {
	-webkit-animation: scale-in-center 0.5s cubic-bezier(0.250, 0.460, 0.450, 0.940) both;
	animation: scale-in-center 0.5s cubic-bezier(0.250, 0.460, 0.450, 0.940) both;
}
@-webkit-keyframes scale-in-center {
  0% {
    -webkit-transform: scale(0);
            transform: scale(0);
    opacity: 1;
  }
  100% {
    -webkit-transform: scale(1);
            transform: scale(1);
    opacity: 1;
  }
}
@keyframes scale-in-center {
  0% {
    -webkit-transform: scale(0);
            transform: scale(0);
    opacity: 1;
  }
  100% {
    -webkit-transform: scale(1);
            transform: scale(1);
    opacity: 1;
  }
}

.scale-out-center {
	-webkit-animation: scale-out-center 0.5s cubic-bezier(0.550, 0.085, 0.680, 0.530) both;
	animation: scale-out-center 0.5s cubic-bezier(0.550, 0.085, 0.680, 0.530) both;
}
@-webkit-keyframes scale-out-center {
  0% {
    -webkit-transform: scale(1);
            transform: scale(1);
    opacity: 1;
  }
  100% {
    -webkit-transform: scale(0);
            transform: scale(0);
    opacity: 1;
  }
}
@keyframes scale-out-center {
  0% {
    -webkit-transform: scale(1);
            transform: scale(1);
    opacity: 1;
  }
  100% {
    -webkit-transform: scale(0);
            transform: scale(0);
    opacity: 1;
  }
}
</style>