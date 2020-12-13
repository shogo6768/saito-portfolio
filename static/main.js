class MobileMenu{
    constructor(){
        this.DOM = {};
        this.DOM.btn = document.querySelector('.mobile-menu__btn');
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

    _addEvent() {
        this.DOM.btn.addEventListener(this.eventType, this._toggle.bind(this));
    }

}

new MobileMenu();

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

