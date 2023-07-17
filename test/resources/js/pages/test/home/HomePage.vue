<template>
  <div class="home-page">

    <saving-component :saving="saving" />

    <h1 class="display-5 fw-bold text-center">
      Zones and Distributions
    </h1>

    <div class="col-lg-6 mx-auto zones mb">
      <zone-editable
        v-for="zone in zones"
        :id="zone.id"
        :name="zone.name"
        :updated_at="zone.updated_at"
        :distributions="zone.distributions"
        :key="zone.uid"
        @edit="zone.name = $event.name; zone.distributions = $event.distributions; zone.updated_at = $event.updated_at"
        @addZone="zone.distributions.push($event.distribution)"
        @saving="changeSavingStatus($event.saving)"
        class="zone"
      />
    </div>

    <h1 class="display-5 fw-bold text-center">
      To Do List
    </h1>

    <ul class="col-lg-6 mx-auto">
      <li style="text-decoration:line-through;">Add the percentage symbol to each distribution number while is not being edited</li>
      <li style="text-decoration:line-through;">The cancel button is not working</li>
      <li style="text-decoration:line-through;">Without refreshing the page, be able to edit all the distributions from a zone</li>
      <li style="text-decoration:line-through;">Be able to add more distributions</li>
      <li style="text-decoration:line-through;">Be able to remove distributions</li>
      <li style="text-decoration:line-through;">When the user is not able to save due to some error, the error must be showed</li>
      <li style="text-decoration:line-through;">The sum of all distributions must be ensured to be 100% in anyway</li>
      <li style="text-decoration:line-through;">The distributions must be integer</li>
      <li style="text-decoration:line-through;">The zone name cannot be empty</li>
      <li style="text-decoration:line-through;">The zone name cannot have more than one space between each word</li>
      <li style="text-decoration:line-through;">The zone name cannot have spaces at start or the end</li>
      <li style="text-decoration:line-through;">The zone name cannot be repeated in any way</li>
      <li style="text-decoration:line-through;">Create a new field "updated_at" that is going to store the date when the name field change</li>
      <li style="text-decoration:line-through;">Show the updated_at field value near each zone name</li>
      <li style="text-decoration:line-through;">Add a way for the user to know that an element is being saved</li>
      <li style="text-decoration:line-through;">When the number of distributions is 5 or greater, the background of that zone must change to any color while is not being edited</li>
    </ul>

  </div>
</template>

<script>
import ZoneEditable from './ZoneEditable.vue';
import SavingComponent from './SavingComponent.vue';

export default {
  name: 'HomePage',
  components: {
    ZoneEditable,
    SavingComponent
  },
  props: {
    context: {
      type: Object
    }
  },
  data() {
    return {
      saving: false,
      zones: [],
      zoneUid: 0
    };
  },
  mounted() {
    this.zones = this.context.zones.map(data => {
      return {
        id: data.id,
        name: data.name,
        updated_at: data.updated_at,
        uid: this.zoneUid++,
        distributions: data.distributions
      };
    });
  },
  methods: {
    changeSavingStatus(newVal) {
        this.saving = newVal;
    }
  }
}
</script>

<style lang="scss">
@import 'resources/scss/variables.scss';

.home-page {
  .zones {
    display: flex;
    gap: 4px;
    flex-direction: column;
  }
}
</style>
