""" Checker for determining text in danger zones around edges """
from slidelint.utils import help_wrapper
from slidelint.pdf_utils import document_pages_layouts, layout_characters

MESSAGES = (
    dict(id='C1003',
         msg_name='too-close-to-edges',
         msg='Too close to edges',
         help='Too close to edges: Text should not appear '
              'closer than 1/12th(by default) of the'
              ' page size to the edges.'), )


@help_wrapper(MESSAGES)
def main(target_file=None, min_page_ratio='12'):
    """ text in danger zones around edges checker """
    rez = check_edges_danger_zone(target_file, min_page_ratio)
    return rez


def check_edges_danger_zone(path, min_page_ratio=12):
    """ Looking through all page layouts for text and comparing it size
    to page size
    """
    # return []
    rez = []
    min_page_ratio = float(min_page_ratio)
    for page_num, page_layout in document_pages_layouts(path):
        width_dist = page_layout.width / min_page_ratio
        height_dist = page_layout.height / min_page_ratio
        # correlation of zero coordinates
        save_zone = (
            width_dist,
            height_dist,
            page_layout.width - width_dist,
            page_layout.height - height_dist)
        # checking save zone
        for character in layout_characters(page_layout):
            legal = (
                save_zone[0] < character.bbox[0],
                save_zone[1] < character.bbox[1],
                save_zone[2] > character.bbox[2],
                save_zone[3] > character.bbox[3])
            if not all(legal):
                rez.append({
                    'id': 'C1003',
                    'page': 'Slide %s' % (page_num + 1),
                    'msg_name': 'too-close-to-edges',
                    'msg': 'Too close to edges: Text should not appear '
                           'closer than 1/%sth of the page size '
                           'to the edges.' % min_page_ratio,
                    'help': 'Too close to edges: Text should not appear '
                            'closer than 1/12th(by default) of the'
                            ' page size to the edges.',
                    })
                break
    return rez
