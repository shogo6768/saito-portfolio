class OpenMenu{
    constructor(){
        this.DOM = {};
        this.DOM.btn = document.querySelector('.mobile-menu__btn');
        this.DOM.cross= document.querySelectorAll('.fa-times');
        this.DOM.side = document.querySelector('.ctg-lists');
        this.DOM.container = document.querySelector('#global-container');
        this.eventType= this._getEventType();
        this._addEvent();
    }


    _getEventType(){
        return window.ontouchstart ? 'touchstart' : 'click'
    }

    _toggle(){
        this.DOM.container.classList.toggle('menu-open')
    }

    // _remove(){
    //     this.DOM.drop.classList.remove('dropDown')
    // }

    _addEvent() {
        this.DOM.btn.addEventListener(this.eventType, this._toggle.bind(this));
        this.DOM.cross[0].addEventListener(this.eventType, this._toggle.bind(this));
        this.DOM.cross[1].addEventListener(this.eventType, this._toggle.bind(this));
        this.DOM.side.addEventListener(this.eventType, this._toggle.bind(this));
        // this.DOM.cross.addEventListener(this.eventType, this._toggle.bind(this));
        // this.DOM.btn.addEventListener(this.eventType, this._remove.bind(this));
        // this.DOM.side.addEventListener(this.eventType, this._remove.bind(this));
    }
}

new OpenMenu();

class DorpDown{
    constructor(){
        this.DOM = {};
        this.DOM.drop = document.querySelectorAll('.category-menu__item > span');
        this.DOM.mDrop = document.querySelectorAll('.mobile-menu__link');
        this.eventType= this._getEventType();
        this._addEvent1();
        this._addEvent2();
        this._addEvent3();
    }

    _getEventType(){
        return window.ontouchstart ? 'touchstart' : 'click'
    }

    _addEvent1() {
        for (let i = 0; i < this.DOM.drop.length; i++) {
        this.DOM.drop[i].addEventListener(this.eventType, function(){
            this.classList.toggle('dropDown');
            this.nextElementSibling.classList.toggle('dropDown');
        });
        }
    }

    _addEvent2() {
        this.DOM.mDrop[2].addEventListener(this.eventType, function(){
            this.classList.toggle('dropDown');
            this.nextElementSibling.classList.toggle('dropDown');
        });
    } 

    _addEvent3() {
        this.DOM.mDrop[3].addEventListener(this.eventType, function(){
            this.classList.toggle('dropDown');
            this.nextElementSibling.classList.toggle('dropDown');
        });
    }   
}

new DorpDown();

class TextAnimation {
    constructor() {
        this.DOM = {};
        this.DOM.el = document.querySelector('.inview');
        this.chars = this.DOM.el.innerHTML.trim().split("");
        this.DOM.el.innerHTML = this._splitText();
    }
    _splitText() {
        return this.chars.reduce((acc, curr) => {
            curr = curr.replace(/\s+/, '&nbsp;');
            return `${acc}<span class="char">${curr}</span>`;
        }, "");
    }

}

new TextAnimation();

