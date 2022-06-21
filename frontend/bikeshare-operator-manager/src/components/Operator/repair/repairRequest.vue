<template>
  <div>
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home' }">home</el-breadcrumb-item>
      <el-breadcrumb-item>Maintenance information</el-breadcrumb-item>
      <el-breadcrumb-item>Repair request</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card>
      <el-row :gutter="20">
      </el-row>
      <el-table :data="repairData" border stripe>
        <el-table-column label="Complaint ID" prop="Complaint_id" width="120px"></el-table-column>
        <el-table-column label="Bike ID" prop="bike_id" width="80px"></el-table-column>
        <el-table-column label="Description" prop="Description" width="100px"></el-table-column>
        <el-table-column label="options" width="120">
          <template slot-scope="scope">
            <el-button @click="handleClick(scope.row)" type="primary" size="small">pick up</el-button>
            <br />
            <el-button @click="errorReport(scope.row)" type="danger" size="small">error report</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div>
        <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="currentPage"
          :page-sizes="[5, 10, 30, 100]" :page-size="pageSize" layout="sizes,jumper" :total="totalnumber">
        </el-pagination>
      </div>
    </el-card>
    <el-dialog title="report" :visible.sync="dialogVisible" width="60%" @close="closeDialog">
      <span slot="footer" class="dialog-footer">
        <el-form ref="form" :model="form" label-width="80px">
          <el-form-item label="Complaint ID">
            <el-input v-model="form.Complaint_id"></el-input>
          </el-form-item>
          <el-form-item label="resolution">
            <el-input v-model="form.resolution"></el-input>
          </el-form-item>
        </el-form>
        <el-button @click="dialogVisible = false">cancel</el-button>
        <el-button type="primary" @click="onSubmit">submit</el-button>
      </span>
    </el-dialog>
  </div>
</template>
<script>
  import qs from 'qs'
  export default {
    data() {
      return {
        currentPage: 1,
        totalnumber: 0,
        pageSize: 5,
        tempList: [],
        Operator_id: 0,
        dialogVisible: false,
        form: {
          resolution: "It is fake",
          Complaint_id: ""
        },
        statusoptions: [{
          value: '1',
          label: 'needs repairing'
        }, {
          value: '2',
          label: 'under repair'
        }, {
          value: '3',
          label: 'repaired'
        }],
        repairData: [],
        value: ''
      }
    },
    methods: {
      handleSizeChange(val) {
        this.pageSize = val;
        this.handleCurrentChange(this.currentPage);
      },
      handleCurrentChange(val) {
        this.currentPage = val;
        this.currentChangePage(this.repairData, this.currentPage)
      },
      currentChangePage(list, currentPage) {
        let from = (currentPage - 1) * this.pageSize;
        let to = currentPage * this.pageSize;
        this.tempList = [];
        for (; from < to; from++) {
          if (list[from]) {
            this.tempList.push(list[from]);
          }
        }
      },
      handleClick(row) {
        let that = this
        console.log(row.bike_id);
        this.Operator_id = this.$session.get("Operator_id")
        var fdata = qs.stringify({
          "bike_id": row.bike_id,
          "operator_id": this.Operator_id
        })
        this.$axios.post('api/operator/repairbike/', fdata).then(function(res) {
          console.log(res);
          that.repairData = []
          that.$message.success(res.data)
          that.$axios.get('api/operator/defectedbikes/').then(function(res) {
            // this.repairData=res.bikesToBeRepaired;
            console.log(res);
            for (var i = 0; i < res.data.length; i++) {
              that.repairData.push(res.data[i].pk)
            }
            that.$data.totalnumber = that.$data.repairData.length;
            that.currentChangePage(that.repairData, 1);
          }).catch(function(error) {
            console.log(error);
          })
        }).catch(function(err) {
          console.log(err);
        })
      },
      errorReport(row) {
        this.dialogVisible = true
        this.form.Complaint_id = row.Complaint_id
      },
      onSubmit() {
        this.$data.dialogVisible = false
        this.Operator_id = this.$session.get("Operator_id")
        let that = this
        var fdata = qs.stringify({
          "complaint_id": this.form.Complaint_id,
          "resolution": this.form.resolution,
          "operator_id":this.Operator_id,
        })
        this.$axios.post('api/operator/invalidatecomplaint/', fdata)
          .then(function(res) {
            console.log("succeed");
            that.$message.success(res.data)
            that.form.Complaint_id = ''
            that.form.resolution = 'It is fake'
            that.repairData = []
            that.$axios.get('api/operator/defectedbikes/').then(function(res) {
              console.log(res);
              for (var i = 0; i < res.data.length; i++) {
                that.repairData.push({
                  bike_id: res.data[i].bike_id,
                  Description: res.data[i].Description,
                  Complaint_id: res.data[i].Complaint_id
                })
              }
              that.$data.totalnumber = that.$data.repairData.length;
              that.currentChangePage(that.repairData, that.currentPage);
            }).catch(function(error) {
              console.log(error);
            })
          }).catch(function(error) {
            console.log(error);
            that.$message.success("failed to report")
          })
      },
      closeDialog() {
        this.form.Complaint_id = ''
        this.form.resolution = 'It is fake'
        console.log(this.$data.form)
      }
    },
    async created() {
      let that = this;
      that.repairData = []
      await this.$axios.get('api/operator/defectedbikes/').then(function(res) {
        console.log(res);
        for (var i = 0; i < res.data.length; i++) {
          that.repairData.push({
            bike_id: res.data[i].bike_id,
            Description: res.data[i].Description,
            Complaint_id: res.data[i].Complaint_id
          })
        }
        that.$data.totalnumber = that.$data.repairData.length;
        that.currentChangePage(that.repairData, that.currentPage);
      }).catch(function(error) {
        console.log(error);
      })

    }
  }
</script>

<style scoped>
.el-card{
	box-shadow: 0 1px 1px rgba(0,0,0,0.15) !important;
}
</style>