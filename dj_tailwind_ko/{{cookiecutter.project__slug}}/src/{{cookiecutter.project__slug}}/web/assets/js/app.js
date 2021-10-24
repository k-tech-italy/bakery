import '../css/style.css';
import ko from 'knockout';


class ItemViewModel {
    constructor() {
        this.items = ko.observableArray([
            { item: 'Ketchup', amount: 2.73 },
            { item: 'Lollipop', amount: 0.50 },
            { item: 'Chocolate', amount: 1.00 }
        ]);

        this.removeItem = value => { this.items.remove(value); };
    }

    addItem() {
        let item = document.getElementsByName('item')[0].value;
        let amount = document.getElementsByName('amount')[0].value;

        if (item !== undefined && amount !== undefined){
            this.items.push({ item: item, amount: amount });
        }
    }
}


ko.applyBindings(new ItemViewModel());
