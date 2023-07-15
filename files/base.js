function _wrapper(domObj) {
  if (!domObj instanceof HTMLElement)
    throw 'Error: Attempting to wrap a non HTMLElement!';
  this.obj = domObj
}
Object.assign(_wrapper.prototype, {
  contains: function() {
    Object.keys(arguments).forEach(k => {
      this.obj.appendChild(arguments[k].obj);
    });
    return this;
  },

  html: function(content) {
    this.obj.innerHTML = content;
    return this;
  },

  setProp: function(obj) {
    Object.keys(obj).forEach(k => {
      this.obj[k] = obj[k];
    });
    return this;
  },

  setAttr: function(obj) {
    Object.keys(obj).forEach(k => {
      this.obj.setAttribute(k, obj[k]);
    });
    return this;
  },

  toggleClass: function(name) {
    this.obj.classList.toggle(name);
    return this;
  },

  addClass: function() {
    Array.from(arguments).forEach((c) => {
      this.obj.classList.add(c);
    });
    return this;
  },

  removeClass: function(name) {
    Array.from(arguments).forEach((c) => {
      this.obj.classList.remove(c);
    });
    return this;
  }
});

const use = id => {
  if (!id) return new _wrapper(document.body);
  const e = document.getElementById(id);
  if (!e) throw `Element ${id} does not exist in document`;
  return new _wrapper(e);
};

const element = name => {
  const e = document.createElement(name);
  if (!e) throw `Element ${name} could not be created`;
  return new _wrapper(e);
};
    
function state(value) {this.value = value}
Object.assign(state.prototype, {
  set: function(value){
    this.onchange?.(value);
    this.value = value;
  },
});

const cx = {

  toast: function(message) {
    return element('div').addClass('toast').contains(
      element('span').html(message),
      element('button').html('\u2715').setProp({onclick: (e) => {
        const container = e.target.parentNode;
        container.parentNode?.removeChild(container);
      }})
    )
  },

}
