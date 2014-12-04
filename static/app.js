/**
 * EmberJS playground.
 */
(function () {

    var emberAppConfig = {
        LOG_TRANSITIONS: true,
        LOG_TRANSITIONS_INTERNAL: true
    };

    window.App = Ember.Application.create(emberAppConfig);

    window.App.Router.map(
        function () {
            this.resource("contacts", {path: "/contacts"});
        }
    );
    window.App.IndexRoute = Ember.Route.extend({beforeModel: function () {this.transitionTo("contacts");}});

    App.Store = DS.Store.extend(
        {
            adapter: DS.RESTAdapter.extend({namespace: 'api'})
        }
    );

    App.Contact = DS.Model.extend(
        {
            nick_name: DS.attr(),
            first_name: DS.attr(),
            last_name: DS.attr(),
            email: DS.attr()
        }
    );

    window.App.ContactsRoute = Ember.Route.extend(
        {
            queryParams: {
                offset: {
                    refreshModel: true
                },
                limit: {
                    refreshModel: true
                }
            },
            meta: {
                offset: 0,
                limit: 10,
                total: 0
            },
            model: function (params) {
                console.log("in route.model, params: ", params);
                //var contacts = this.store.filter("contact", params, function(x){return x.get("id");});
                var contacts = this.store.find("contact", params);

                var meta = this.store.metadataFor("contact");
                //var meta = contacts.get("content.meta");
                console.log("metadata: ", meta);

                this.set("meta.offset", meta.offset);
                this.set("meta.limit", meta.limit);
                this.set("meta.total", meta.total);

                return contacts;
            },
            setupController: function (controller, contacts) {
                this._super(controller, contacts);

                var meta = this.store.metadataFor("contact");
                //var meta = contacts.get("content.meta");
                console.log("metadata: ", meta);

                this.set("meta.offset", meta.offset);
                this.set("meta.limit", meta.limit);
                this.set("meta.total", meta.total);

                controller.set("offset", this.meta.offset);
                controller.set("limit", this.meta.limit);
                controller.set("total", this.meta.total);
            }
        }
    );

    window.App.ContactsController = Ember.ArrayController.extend(
        {
            queryParams: ["offset", "limit"],
            offset: 0,
            limit: 10,
            total: 0,
            new_contact: {
                nick_name: "",
                first_name: "",
                last_name: "",
                email: ""
            },
            noPrev: function() {
                return this.offset <= 0;
            }.property("offset"),
            noNext: function() {
                return (this.offset + this.limit) >= this.total;
            }.property("offset", "limit", "total"),
            actions: {
                prev: function () {
                    var offset = this.offset - this.limit;
                    if (offset < 0) {
                        offset = 0;
                    }
                    this.set("offset", offset);
                },
                next: function () {
                    var offset = this.offset + this.limit;
                    this.set("offset", offset);
                },
                remove: function (contact) {
                    contact.deleteRecord();
                    contact.save();
                },
                clear: function () {
                    Ember.set(this.new_contact, "nick_name", "");
                    Ember.set(this.new_contact, "first_name", "");
                    Ember.set(this.new_contact, "last_name", "");
                    Ember.set(this.new_contact, "email", "");
                },
                create: function () {
                    console.log(this.new_contact);
                    var contact = this.store.createRecord("contact", this.new_contact);
                    contact.save();
                }
            }
        }
    );

})();
