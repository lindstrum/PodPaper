/**
 * Defines an HTML tag for a loading page
 */
customElements.define("loading-page", class extends HTMLElement {
    constructor() {
        super();

        //load html
        const panel_layout_template = document.getElementById("audio_panel_template"); //Imported in index.html
        this.panel = panel_layout_template.content.cloneNode(true);

        //load css
        const style_link = document.createElement('link');
        style_link.setAttribute('rel', 'stylesheet');
        style_link.setAttribute('href', 'audio_panel_style.css');

        //load DOM
        const root = this.attachShadow({mode: "open"});
        root.appendChild(style_link);
        root.appendChild(panel);
    }

    /**
     * Assigns a callback function to a DOM element that will be triggered when the user clicks on the element
     *
     * @param id_of_element value of id attribute of the element
     * @param callableFunction function to execute when the user clicks on the element
     * @throws when either parameter is an invalid type or when there is no element in the DOM with the given id
     */
    set_onclick_function_by_id(id_of_element, callableFunction) {
        if (typeof id_of_element !== "string") {
            throw new Error("Invalid id: " + id_of_element);
        } else if (id_of_element.length === 0) {
            throw new Error("Id given is empty.")
        } else if (typeof callableFunction !== "function") {
            throw new Error("No function was given as a callback.")
        } else {
            const element = this.panel.querySelector(`#${id_of_element}`);
            if (element != null) {
                element.onclick = callableFunction;
            } else {
                throw new Error(`Could not assign onclick function to \"${id_of_element}\" because no element in the DOM exists with this id.`);
            }
        }
    }
});