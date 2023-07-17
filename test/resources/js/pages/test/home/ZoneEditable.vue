<template>
  <div
  	class="zone-editable"
	:class="{greatherThanFive: (this.distributions.length >= 5 && display)}"
	>
    <div
      v-if="display"
      class="zone-display"
    >
      <div>
        Zone Name: <strong>{{ name }}</strong> Distributions: {{ distributionDisplay }}
      </div>

        <div class="zone-button">

            <button
                class="btn btn-primary"
                @click="setDisplayEdit(false)"
                :disabled="saving"
            >
                Edit
            </button>

            <button
                class="btn btn-success"
                @click="setDisplayAddDistribution(false)"
                :disabled="saving"
            >
                Add distribution
            </button>

        </div>

    </div>
    <div
        v-else-if="displayAddDistributionForm"
    >

        <div class="zone-edit">
            <label class="control-label">
                Distribution
            </label>

            <input
                v-model="distributionToAdd"
				type="number"
				step="1"
				min="1"
				:max="distributionToAdd"
				@keyup="isDistributionToAddIsGreatherThanTheMaxAmount"
                placeholder="Percentage"
            >

            <div class="zone-edit-actions">

                <button
                class="btn btn-secondary"
                @click="display = true; displayAddDistributionForm = false;"
                :disabled="saving"
                >
                Cancel
                </button>

                <button
                class="btn btn-success"
                @click="addNewDistribution"
                :disabled="saving"
                >
                Save
                </button>

            </div>

        </div>

    </div>

    <div
      v-else
      class="zone-edit"
    >
      <label class="control-label">
        Zone Name
      </label>

      <input
        v-model="form.name"
		type="string"
        placeholder="Zone name"
        class="form-control"
        :disabled="saving"
      >

      <div class="zone-edit-distributions">
        <div v-for="distribution in form.distributions">
          <label class="control-label label-distribution">
            Distribution
          </label>

          <input
            v-model="distribution.percentage"
			type="number"
			step="1"
			min="1"
            placeholder="Percentage"
            class="form-control percentage-input"
          >

        <input
            v-model="distribution.delete"
            type="checkbox"
            class="btn-check"
            :id="'distribution_delete_' + distribution.id"
            autocomplete="off">
        <label class="btn btn-outline-primary delete-button" :for="'distribution_delete_' + distribution.id">Delete</label>

        </div>
      </div>

      <div class="zone-edit-actions">
        <button
          class="btn btn-secondary"
          @click="display = true"
          :disabled="saving"
        >
         Cancel
        </button>

        <button
          class="btn btn-success"
          @click="save"
          :disabled="saving"
        >
          Save
        </button>
      </div>
    </div>

	<div v-if="updated_at_string">
	Updated date: {{ updated_at_string }}
	</div>

  </div>
</template>

<script>
export default {
  name: 'ZoneEditable',
  props: {
    name: String,
    id: Number,
	updated_at: String,
    distributions: Array,
  },
  watch: {
	updated_at: function (newVal, oldVal) {
		this.updated_at_string = new Date(newVal);
		this.updated_at_string = `${this.updated_at_string.getHours()}:${(this.updated_at_string.getMinutes()<10?'0':'') + this.updated_at_string.getMinutes()}:${this.updated_at_string.getSeconds()} ${this.updated_at_string.getDate()}/${this.updated_at_string.getMonth()}/${this.updated_at_string.getFullYear()}`;
	},
	saving: function (newVal, oldVal) {

		if (newVal == false) {
			// little effect
			setTimeout(() => {
				this.$emit('saving', {saving: newVal});
			}, 300);
		} else {
			this.$emit('saving', {saving: newVal});
		}

	}
  },
  data() {
    return {
      display: true,
      displayAddDistributionForm: false,
      distributionToAdd: 0,
	  maxDistributionLimit: 0,
	  actualFormIsValid: true,
	  updated_at_string: '',
      form: {
        name: '',
        distributions: [],
      },
      saving: false
    };
  },
  computed: {
    distributionDisplay() {
      return this.distributions.map(distribution => `${distribution.percentage}%`).join('-');
    }
  },
  mounted() {
    this.getValuesFromProps();
  },
  methods: {
	validation(option, shouldBe, variable) {
		console.log(option, shouldBe, typeof variable);
		if (option == 'typeof') {
			return (typeof variable == shouldBe) ? true : false;
		}
		if (option == 'empty') {
			console.log(variable.length);
			return (variable.length != 0) ? true : false;
		}

	},
	sanitizer(option, variable) {
		if (option == 'duplicated_spaces') {
			while (variable.indexOf('  ') > -1) {
				variable = variable.replace('  ', ' ');
			}
			return variable.trim();
		}
	},
    getValuesFromProps() {
      this.form.name = this.name;
	  this.setAndFormatUpdatedAtDate();
	  this.form.distributions = this.distributions.map(distribution => {
        return {
          id: distribution.id,
          percentage: distribution.percentage
        };
      });
    },
	setAndFormatUpdatedAtDate() {
		this.updated_at_string = new Date(this.updated_at);
		this.updated_at_string = `${this.updated_at_string.getHours()}:${(this.updated_at_string.getMinutes()<10?'0':'') + this.updated_at_string.getMinutes()}:${this.updated_at_string.getSeconds()} ${this.updated_at_string.getDate()}/${this.updated_at_string.getMonth()}/${this.updated_at_string.getFullYear()}`;
	},
    setDisplayEdit(value) {
      this.display = value;

      if(!this.display) {
        this.getValuesFromProps();
      }
    },
    setDisplayAddDistribution(value) {
      this.display = value;
      this.displayAddDistributionForm = true;

	  let maxDistributionLimit = 100;

      if(!this.display) {

		this.getValuesFromProps();

		this.distributions.forEach((distribution) => {

			maxDistributionLimit -= Number(distribution.percentage);

		});

		this.distributionToAdd = maxDistributionLimit;
		this.maxDistributionLimit = maxDistributionLimit;

		if (this.maxDistributionLimit == 0) {
	        alertify.alert('Limit amount reached', `100% reached, remove an amount to disperse again`);
			this.display = true;
			this.displayAddDistributionForm = false;
		}

      }
    },
	isDistributionToAddIsGreatherThanTheMaxAmount() {
		if (this.distributionToAdd > this.maxDistributionLimit) {
			this.distributionToAdd = Number(this.maxDistributionLimit);
		} else {
			this.distributionToAdd = Number(this.distributionToAdd);
		}
	},
	resetDistributionToAdd() {
		this.distributionToAdd = this.maxDistributionLimit;
	},
    async save() {

      this.saving = true;

      const params = {
        id: this.id,
        name: this.form.name,
        distributions: this.form.distributions
      };

	if (!this.validation('empty', params.name, params.name)) {
		alertify.alert('Validation error', 'Zone name cannot be empty');
		this.saving = false;
		return;
	}

	// sanitize name to remove two spaces and trim
	params.name = this.sanitizer('duplicated_spaces', params.name);

	let distributionSum = 0;
	params.distributions.forEach((distribution) => {
		distribution.percentage = Number(distribution.percentage);
		if (!this.validation('typeof', 'number', distribution.percentage)) {
			// refactor
			this.actualFormIsValid = false;
			this.saving = false;
		}

		distributionSum += distribution.percentage;
	});

	if (!this.actualFormIsValid) {
		alertify.alert('Validation error', 'Distribution should be numeric');
		this.resetDistributionToAdd();
		this.actualFormIsValid = true;
		return;
	}

	if (distributionSum > 100) {
		alertify.alert('Limit amount reached', `100% reached, remove an amount to disperse again`);
		this.saving = false;
		return;
	}

	let response = await axios.post('/api/zones/edit', params).catch((err) => {
        alertify.alert(err.message, `${err.response.data}. Contact a system administrator.`);
        return;
	});

      this.saving = false;
      this.display = true;

    if (response == undefined) { return; }

	console.log(response.data);

     // Check and omit deleted distributions
     let new_distributions = this.form.distributions.filter(distribution => { return !distribution.hasOwnProperty('delete'); } );

    this.form.distributions = new_distributions;

      this.$emit('edit', {
        name: params.name,
		updated_at: response.data,
        distributions: this.form.distributions
      });

    },
    async addNewDistribution() {
      this.saving = true;

      const params = {
        zone: this.id,
        distribution: this.distributionToAdd
      };

	if (!this.validation('typeof', 'number', params.distribution)) {
        alertify.alert('Validation error', 'Distribution should be numeric');
		this.resetDistributionToAdd();

		// refactor
		this.saving = false;
		return;
	}

      let response = await axios.post('/api/zones/distribution/add', params).catch((err) => {
        alertify.alert(err.message, `${err.response.data}. Contact a system administrator.`);
        return;
	  });

		this.saving = false;
		this.display = true;
		this.distributionToAdd = 0;
		this.displayAddDistributionForm = false;

		if (response == undefined) { return; }

		this.$emit('addZone', {
			distribution: response.data
		});

	}
  }
}
</script>

<style lang="scss">
@import 'resources/scss/variables.scss';

  .greatherThanFive {
	background-color: $greater-than-five-background-color;
	border: 1px $greater-than-five-border solid;
	color: $greater-than-five-color;
  }

.zone-editable {
  border: 1px solid $gray-color;
  padding: $qmb;
  border-radius: $border-radius;

  .zone-display {
    display: flex;
    align-items: center;
    justify-content: space-between;

    .zone-button {
        width: 30%;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
    }

  }

  .zone-edit {
    display: flex;
    flex-direction: column;
    gap: $small-action-space;

    .zone-edit-actions {
      display: flex;
      gap: $small-action-space;
      justify-content: end;
      margin-top: 10px;
    }

    .zone-edit-distributions {
      display: grid;
      grid-template-columns: repeat(1, 1fr);
      gap: $small-action-space;

      div {

        width: 100%;
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;

        .label-distribution {
            width: 100%;
        }

        .percentage-input {
            width: 70%;
        }

        .delete-button {
            width: 20%;
        }

      }

    }



  }
}
</style>
